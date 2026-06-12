<?php
// =====================
// hoop.php - save user
// =====================

if ($_SERVER['REQUEST_METHOD'] !== 'POST') {
    echo json_encode(['success' => false, 'message' => 'متد اشتباه']);
    exit;
}

function clean($data) {
    $data = trim($data);
    $data = stripslashes($data);
    $data = htmlspecialchars($data, ENT_QUOTES, 'UTF-8');
    return $data;
}

$first_name = isset($_POST['first_name']) ? clean($_POST['first_name']) : '';
$last_name  = isset($_POST['last_name']) ? clean($_POST['last_name']) : '';
$phone      = isset($_POST['phone']) ? clean($_POST['phone']) : '';

$errors = [];

if (empty($first_name) || mb_strlen($first_name, 'UTF-8') < 2) {
    $errors['first_name'] = 'نام باید حداقل ۲ حرف باشد';
}
if (empty($last_name) || mb_strlen($last_name, 'UTF-8') < 2) {
    $errors['last_name'] = 'نام خانوادگی باید حداقل ۲ حرف باشد';
}
if (!preg_match('/^09\d{9}$/', $phone)) {
    $errors['phone'] = 'شماره تلفن معتبر نیست (مثال: 09123456789)';
}

if (!empty($errors)) {
    echo json_encode(['success' => false, 'message' => 'لطفاً خطاها را بررسی کنید', 'errors' => $errors], JSON_UNESCAPED_UNICODE);
    exit;
}

$file = 'users_data.json';
$users = [];
if (file_exists($file)) {
    $json = file_get_contents($file);
    $users = json_decode($json, true);
    if (!is_array($users)) $users = [];
}

// چک تکراری
foreach ($users as $u) {
    if (isset($u['phone']) && $u['phone'] === $phone) {
        echo json_encode(['success' => false, 'message' => 'این شماره قبلاً ثبت شده', 'errors' => ['phone' => 'شماره تکراری']], JSON_UNESCAPED_UNICODE);
        exit;
    }
}

$newUser = [
    'id' => count($users) + 1,
    'first_name' => $first_name,
    'last_name' => $last_name,
    'phone' => $phone,
    'time' => date('Y-m-d H:i:s')
];
$users[] = $newUser;

file_put_contents($file, json_encode($users, JSON_UNESCAPED_UNICODE | JSON_PRETTY_PRINT), LOCK_EX);

echo json_encode([
    'success' => true,
    'message' => $first_name . ' ' . $last_name . ' عزیز، ثبت‌نام انجام شد'
], JSON_UNESCAPED_UNICODE);
exit;