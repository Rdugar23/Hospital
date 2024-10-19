<?php
try {
    // Подключение к базе данных SQLite
    $db = new PDO('sqlite:database.sqlite');
    $db->setAttribute(PDO::ATTR_ERRMODE, PDO::ERRMODE_EXCEPTION);

    // Получение данных из формы
    $clientName = $_POST['client_name'];
    $doctor = $_POST['doctor'];
    $appointmentTime = $_POST['appointment_time'];
    $email = $_POST['email'];
    $phone = $_POST['phone'];
    $address = $_POST['address'];
    $policy = $_POST['policy'];
    $snils = $_POST['snils'];

    // SQL-запрос на вставку данных в таблицу appointments
    $sql = "INSERT INTO appointments 
            (client_name, doctor, appointment_time, email, phone, address, policy, snils) 
            VALUES 
            (:client_name, :doctor, :appointment_time, :email, :phone, :address, :policy, :snils)";

    // Подготовка и выполнение запроса
    $stmt = $db->prepare($sql);
    $stmt->execute([
        ':client_name' => $clientName,
        ':doctor' => $doctor,
        ':appointment_time' => $appointmentTime,
        ':email' => $email,
        ':phone' => $phone,
        ':address' => $address,
        ':policy' => $policy,
        ':snils' => $snils
    ]);

    // Перенаправление на 1111.php с параметрами
    header("Location: 1111.php?success=1&name=" . urlencode($clientName) . "&time=" . urlencode($appointmentTime));
    exit; // Завершаем выполнение скрипта после перенаправления
} catch (PDOException $e) {
    echo "Ошибка: " . $e->getMessage();
}
?>
