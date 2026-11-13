<?php
/**
 * Migración inicial: aplica los esquemas y carga seed_winep3dia.json en winep3dia_db.
 * Uso (en el servidor, por CLI):  php migrate.php
 * Idempotente: usa INSERT ... ON DUPLICATE KEY UPDATE por slug.
 */
if (PHP_SAPI !== 'cli') { http_response_code(403); exit("CLI only\n"); }

$cfg = require '/var/www/vhosts/jreyes13.net/private/db_config.php';

function pdo(array $c): PDO {
    return new PDO("mysql:host={$c['host']};dbname={$c['name']};charset=utf8mb4", $c['user'], $c['pass'], [
        PDO::ATTR_ERRMODE => PDO::ERRMODE_EXCEPTION,
        PDO::ATTR_DEFAULT_FETCH_MODE => PDO::FETCH_ASSOC,
    ]);
}
function runSqlFile(PDO $db, string $file): void {
    $sql = file_get_contents($file);
    $sql = preg_replace('/^\s*--.*$/m', '', $sql);
    foreach (array_filter(array_map('trim', explode(';', $sql))) as $stmt) $db->exec($stmt);
}
function slugify(string $s): string {
    $s = iconv('UTF-8', 'ASCII//TRANSLIT//IGNORE', $s);
    $s = strtolower(preg_replace('/[^A-Za-z0-9]+/', '-', $s));
    return trim(substr($s, 0, 110), '-');
}
function j($v) { return $v === null ? null : json_encode($v, JSON_UNESCAPED_UNICODE); }

$dir = __DIR__;
$adm = pdo($cfg['admin_db']);
$wp  = pdo($cfg['winep3dia_rw']);

runSqlFile($adm, "$dir/../sql/admin_db.sql");
runSqlFile($wp,  "$dir/../sql/winep3dia_db.sql");
echo "Esquemas aplicados.\n";

$seed = json_decode(file_get_contents("$dir/seed_winep3dia.json"), true, 512, JSON_THROW_ON_ERROR);

$catStmt = $wp->prepare("INSERT INTO categories (slug,name_es,name_en) VALUES (?,?,?)
                         ON DUPLICATE KEY UPDATE name_es=VALUES(name_es), name_en=COALESCE(VALUES(name_en),name_en)");
$catId = function (?string $es, ?string $en) use ($wp, $catStmt) {
    if (!$es) return null;
    $slug = slugify($es);
    $catStmt->execute([$slug, $es, $en]);
    $q = $wp->prepare("SELECT id FROM categories WHERE slug=?"); $q->execute([$slug]);
    return (int)$q->fetchColumn();
};

$wp->beginTransaction();

$art = $wp->prepare("INSERT INTO articles (slug,standard_code,category_id,badge_color,title_es,title_en,summary_es,summary_en,
  content_es,content_en,key_takeaways_es,key_takeaways_en,related_grapes,related_regions,tags,status,updated_by)
  VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,'published','migration')
  ON DUPLICATE KEY UPDATE standard_code=VALUES(standard_code),category_id=VALUES(category_id),badge_color=VALUES(badge_color),
  title_es=VALUES(title_es),title_en=VALUES(title_en),summary_es=VALUES(summary_es),summary_en=VALUES(summary_en),
  content_es=VALUES(content_es),content_en=VALUES(content_en),key_takeaways_es=VALUES(key_takeaways_es),
  key_takeaways_en=VALUES(key_takeaways_en),related_grapes=VALUES(related_grapes),related_regions=VALUES(related_regions),
  tags=VALUES(tags),updated_by='migration'");
foreach ($seed['articles'] as $a) {
    $art->execute([$a['id'], $a['standard'], $catId($a['category_es'] ?? null, $a['category_en'] ?? null),
        $a['badge_color'] ?? 'slate', $a['title_es'], $a['title_en'] ?? null, $a['summary_es'] ?? null, $a['summary_en'] ?? null,
        $a['content_es'] ?? null, $a['content_en'] ?? null, j($a['key_takeaways_es'] ?? null), j($a['key_takeaways_en'] ?? null),
        j($a['related_grapes'] ?? null), j($a['related_regions'] ?? null), j($a['tags'] ?? null)]);
}

$card = $wp->prepare("INSERT INTO cards (slug,standard_code,category_id,question_es,answer_es,solution_es,citation,status,updated_by)
  VALUES (?,?,?,?,?,?,?,'published','migration')
  ON DUPLICATE KEY UPDATE standard_code=VALUES(standard_code),category_id=VALUES(category_id),question_es=VALUES(question_es),
  answer_es=VALUES(answer_es),solution_es=VALUES(solution_es),citation=VALUES(citation),updated_by='migration'");
foreach ($seed['cards'] as $c) {
    $card->execute([$c['id'], $c['standard'], $catId($c['category'] ?? null, null),
        $c['question_es'], $c['answer_es'], $c['solution_es'] ?? null, $c['citation'] ?? null]);
}

$src = $wp->prepare("INSERT INTO sources (slug,title,authors,publisher,kind,url,label_es,label_en,note_es,note_en,sort_order)
  VALUES (?,?,?,?,?,?,?,?,?,?,?)
  ON DUPLICATE KEY UPDATE title=VALUES(title),authors=VALUES(authors),publisher=VALUES(publisher),kind=VALUES(kind),url=VALUES(url),
  label_es=VALUES(label_es),label_en=VALUES(label_en),note_es=VALUES(note_es),note_en=VALUES(note_en),sort_order=VALUES(sort_order)");
foreach ($seed['sources'] as $s) {
    $src->execute([$s['slug'], $s['title'], $s['authors'], $s['publisher'], $s['kind'], $s['url'],
        $s['label_es'], $s['label_en'], $s['note_es'], $s['note_en'], $s['sort_order']]);
}

$wp->commit();

foreach (['standards','categories','articles','cards','sources'] as $t) {
    printf("%-11s %d\n", $t, $wp->query("SELECT COUNT(*) FROM $t")->fetchColumn());
}
echo "Por estándar (artículos / fichas):\n";
foreach ($wp->query("SELECT s.code,
    (SELECT COUNT(*) FROM articles a WHERE a.standard_code=s.code) arts,
    (SELECT COUNT(*) FROM cards c WHERE c.standard_code=s.code) cards FROM standards s ORDER BY sort_order") as $r) {
    printf("  %-6s %d / %d\n", $r['code'], $r['arts'], $r['cards']);
}
