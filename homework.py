class InfoMessage:
    """Информационное сообщение о тренировке."""
    def __init__(
            self, training_type: str, duration: float,
            distance: float, speed: float, calories: float):
        self.training_type = training_type
        self.duration = duration
        self.distance = distance
        self.speed = speed
        self.calories = calories

    def get_message(self) -> str:
        duration = '%.3f' % round(self.duration, 3)
        distance = '%.3f' % round(self.distance, 3)
        speed = '%.3f' % round(self.speed, 3)
        calories = '%.3f' % round(self.calories, 3)
        return (f'Тип тренировки: {self.training_type}; '
                f'Длительность: {duration} ч.; '
                f'Дистанция: {distance} км; '
                f'Ср. скорость: {speed} км/ч; '
                f'Потрачено ккал: {calories}.')


class Training:
    """Базовый класс тренировки."""
    LEN_STEP = 0.65
    M_IN_KM = 1000
    MINUTES_IN_HOUR = 60

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 ) -> None:
        self.action = action
        self.duration = duration
        self.weight = weight

    def get_distance(self) -> float:
        """Получить дистанцию в км."""
        return self.action * self.LEN_STEP / self.M_IN_KM

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""
        return self.get_distance() / self.duration

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        pass

    def show_training_info(self) -> InfoMessage:
        """Вернуть информационное сообщение о выполненной тренировке."""
        distance = self.get_distance()
        speed = self.get_mean_speed()
        calories = self.get_spent_calories()
        return InfoMessage(
            self.__class__.__name__,
            self.duration,
            distance,
            speed,
            calories
        )


class Running(Training):
    """Тренировка: бег."""
    CALORIES_MEAN_SPEED_MULTIPLIER = 18
    CALORIES_MEAN_SPEED_SHIFT = 1.79

    def get_spent_calories(self) -> float:
        spent_calories = (
            (self.CALORIES_MEAN_SPEED_MULTIPLIER
             * self.get_mean_speed()
             + self.CALORIES_MEAN_SPEED_SHIFT)
            * self.weight / self.M_IN_KM
            * self.duration * self.MINUTES_IN_HOUR)
        return spent_calories


class SportsWalking(Training):
    """Тренировка: спортивная ходьба."""
    CALORIES_WEIGHT_MULTIPLIER_FIRST = 0.035
    CALORIES_WEIGHT_MULTIPLIER_SECOND = 0.029
    M_IN_SEC = 0.278
    SM_IN_M = 100

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 height: float) -> None:
        super().__init__(action, duration, weight)
        self.height = height

    def get_spent_calories(self) -> float:
        speed_in_sec = self.get_mean_speed() * self.M_IN_SEC
        height_in_m = self.height / self.SM_IN_M
        duration_in_min = self.duration * self.MINUTES_IN_HOUR
        return ((self.CALORIES_WEIGHT_MULTIPLIER_FIRST * self.weight
                + (speed_in_sec**2 / height_in_m)
                * self.CALORIES_WEIGHT_MULTIPLIER_SECOND * self.weight)
                * duration_in_min)


class Swimming(Training):
    """Тренировка: плавание."""
    LEN_STEP = 1.38
    SPEED_COEFFICIENT = 1.1
    SPEED_MULTIPLE = 2

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 length_pool: float,
                 count_pool: int) -> None:
        super().__init__(action, duration, weight)
        self.length_pool = length_pool
        self.count_pool = count_pool

    def get_mean_speed(self):
        return (self.length_pool * self.count_pool
                / self.M_IN_KM / self.duration)

    def get_spent_calories(self):
        return ((self.get_mean_speed() + self.SPEED_COEFFICIENT)
                * self.SPEED_MULTIPLE * self.weight * self.duration)


def read_package(workout_type: str, data: list) -> Training:
    """Прочитать данные полученные от датчиков."""
    training_dict = {
        'SWM': Swimming,
        'RUN': Running,
        'WLK': SportsWalking
    }
    return (training_dict.get(workout_type)(*data)
            if training_dict.get(workout_type) else None)


def main(training: Training) -> None:
    """Главная функция."""
    info = training.show_training_info()
    print(info.get_message())


if __name__ == '__main__':
    packages = [
        ('SWM', [720, 1, 80, 25, 40]),
        ('RUN', [15000, 1, 75]),
        ('WLK', [9000, 1, 75, 180]),
    ]

    for workout_type, data in packages:
        training = read_package(workout_type, data)
        main(training)
