from dataclasses import asdict, dataclass


@dataclass
class InfoMessage:
    """Информационное сообщение о тренировке."""
    training_type: str
    duration: float
    distance: float
    speed: float
    calories: float

    message_output = ('Тип тренировки: {training_type}; '
                      'Длительность: {duration:.3f} ч.; '
                      'Дистанция: {distance:.3f} км; '
                      'Ср. скорость: {speed:.3f} км/ч; '
                      'Потрачено ккал: {calories:.3f}.')

    def get_message(self) -> str:
        return self.message_output.format(**asdict(self))


class Training:
    """Базовый класс тренировки."""
    LEN_STEP: float = 0.65
    M_IN_KM: float = 1000
    HOUR_TO_MIN: int = 60

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
        return (self.action * self.LEN_STEP / self.M_IN_KM)

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""
        return (self.get_distance() / self.duration)

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        raise NotImplementedError

    def show_training_info(self) -> InfoMessage:
        """Вернуть информационное сообщение о выполненной тренировке."""
        return InfoMessage(self.__class__.__name__,
                           self.duration, self.get_distance(),
                           self.get_mean_speed(), self.get_spent_calories())


class Running(Training):
    """Тренировка: бег."""
    coeff_calorie_running_one = 18
    coeff_calorie_running_two = 20

    def get_spent_calories(self) -> float:
        return ((self.coeff_calorie_running_one * self.get_mean_speed()
                - self.coeff_calorie_running_two)
                * self.weight / self.M_IN_KM
                * (self.duration * self.HOUR_TO_MIN))


class SportsWalking(Training):
    """Тренировка: спортивная ходьба."""
    coeff_calorie_sportwalking_one = 0.035
    coeff_calorie_sportwalking_two = 0.029

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 height: float
                 ) -> None:
        super().__init__(action, duration, weight)
        self.height = height

    def get_spent_calories(self) -> float:
        return ((self.coeff_calorie_sportwalking_one
                * self.weight + (self.get_mean_speed()**2 // self.height)
                * self.coeff_calorie_sportwalking_two * self.weight)
                * (self.duration * self.HOUR_TO_MIN))


class Swimming(Training):
    """Тренировка: плавание."""
    LEN_STEP = 1.38
    coeff_calorie_swimming_one = 1.1
    coeff_calorie_swimming_two = 2

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 length_pool: float,
                 count_pool: float
                 ) -> None:
        super().__init__(action, duration, weight)
        self.length_pool = length_pool
        self.count_pool = count_pool

    def get_distance(self) -> float:
        return (self.action * self.LEN_STEP / self.M_IN_KM)

    def get_mean_speed(self) -> float:
        return (self.length_pool * self.count_pool / self.M_IN_KM
                / self.duration)

    def get_spent_calories(self) -> float:
        return ((self.get_mean_speed() + self.coeff_calorie_swimming_one)
                * self.coeff_calorie_swimming_two * self.weight)


def read_package(workout_type: str, data: list) -> Training:
    """Прочитать данные полученные от датчиков."""
    try:
        workout_code = {
            "SWM": Swimming,
            "RUN": Running,
            "WLK": SportsWalking
        }
        return workout_code[workout_type](*data)
    except ValueError:
        raise Exception('Error')


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
