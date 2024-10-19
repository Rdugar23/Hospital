<!DOCTYPE html>
<html lang="en">
<head>
    <title>Запись на прием - Travel Agency</title>
    <meta property="og:title" content="Запись на прием - Travel Agency" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <meta charset="utf-8" />
    <link rel="stylesheet" href="https://unpkg.com/animate.css@4.1.1/animate.css" />
    <link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Poppins&display=swap" />
    <style>
        body {
            font-family: 'Poppins', sans-serif;
            background-color: #f4f4f4;
            color: #333;
        }
        .form-container {
            width: 500px;
            margin: 50px auto;
            padding: 20px;
            background-color: #fff;
            border-radius: 10px;
            box-shadow: 0 0 10px rgba(0,0,0,0.1);
        }
        .form-group {
            margin-bottom: 15px;
        }
        .form-group label {
            display: block;
            margin-bottom: 5px;
        }
        .form-group input, .form-group select {
            width: 100%;
            padding: 8px;
            box-sizing: border-box;
        }
        .submit-button {
            width: 100%;
            padding: 10px;
            background-color: #28a745;
            color: white;
            border: none;
            border-radius: 5px;
            cursor: pointer;
        }
        .home-button {
            margin-top: 20px;
            width: 100%;
            padding: 10px;
            background-color: #007bff;
            color: white;
            border: none;
            border-radius: 5px;
            cursor: pointer;
            text-align: center;
            text-decoration: none;
            display: block;
        }
        .notification {
            background-color: #dff0d8;
            color: #3c763d;
            padding: 15px;
            margin-bottom: 20px;
            border: 1px solid #d6e9c6;
            border-radius: 4px;
        }
    </style>
</head>
<body>

<div class="form-container">
    <h2>Запись на прием</h2>
    
    <?php
    // Проверка, был ли успешный переход с записью
    if (isset($_GET['success']) && $_GET['success'] == 1) {
        // Получаем имя клиента и время записи из URL
        $name = htmlspecialchars($_GET['name']);
        $time = htmlspecialchars($_GET['time']);
        $formattedTime = date('d.m.Y H:i', strtotime($time)); // Форматируем дату и время

        // Выводим уведомление об успешной записи
        echo "<div class='notification'>";
        echo "Запись успешно добавлена! Ждем вас, $name, на приеме в $formattedTime.";
        echo "</div>";
    }
    ?>
    
    <?php include 'load_doctors.php'; ?>
    <form action="submit_appointment.php" method="POST" class="appointment-form">
        <div class="form-group">
            <label for="client-name">Имя клиента:</label>
            <input type="text" id="client-name" name="client_name" required />
        </div>
        <div class="form-group">
            <label for="doctor">Выберите врача:</label>
            <select id="doctor" name="doctor" required>
                <?php foreach ($doctors as $doctor): ?>
                    <option value="<?php echo $doctor['doctor_name'] . ' (' . $doctor['specialty'] . ')'; ?>">
                        <?php echo $doctor['doctor_name'] . ' (' . $doctor['specialty'] . ') - Время работы: ' . $doctor['work_start'] . '-' . $doctor['work_end']; ?>
                    </option>
                <?php endforeach; ?>
            </select>
        </div>
        <div class="form-group">
            <label for="appointment-time">Дата и время записи:</label>
            <input type="datetime-local" id="appointment-time" name="appointment_time" required />
        </div>
        <div class="form-group">
            <label for="email">Электронная почта:</label>
            <input type="email" id="email" name="email" required />
        </div>
        <div class="form-group">
            <label for="phone">Номер телефона:</label>
            <input type="tel" id="phone" name="phone" required />
        </div>
        <div class="form-group">
            <label for="address">Прописка:</label>
            <input type="text" id="address" name="address" required />
        </div>
        <div class="form-group">
            <label for="policy">Страховой полис:</label>
            <input type="text" id="policy" name="policy" required />
        </div>
        <div class="form-group">
            <label for="snils">СНИЛС:</label>
            <input type="text" id="snils" name="snils" required />
        </div>
        <button type="submit" class="submit-button">Записаться</button>
    </form>

    <!-- Кнопка для перехода на главную страницу -->
    <a href="index.html" class="home-button">На главную</a>
</div>

</body>
</html>
