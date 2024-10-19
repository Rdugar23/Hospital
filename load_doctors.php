<?php
try {
    // Подключение к базе данных SQLite
    $db = new PDO('sqlite:database.sqlite');
    $db->setAttribute(PDO::ATTR_ERRMODE, PDO::ERRMODE_EXCEPTION);

    // Получение списка врачей из базы данных
    $sql = "SELECT doctor_name, specialty, work_start, work_end FROM doctors";
    $stmt = $db->prepare($sql);
    $stmt->execute();
    $doctors = $stmt->fetchAll(PDO::FETCH_ASSOC);

    // Проверим, если массив пустой
    if (empty($doctors)) {
        echo "Нет данных о врачах.";
    }

} catch (PDOException $e) {
    echo "Ошибка: " . $e->getMessage();
    exit;
}
?>
