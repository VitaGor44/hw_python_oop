from typing import List, Dict
from dataclasses import dataclass
from dataclasses import asdict


@dataclass
class InfoMessage():
    """Информационное сообщение о тренировке."""
    training_type: str
    duration: float
    distance: float
    speed: float
    calories: float
    MESSAGE: str = (
        "Тип тренировки: {training_type};"
        "Длительность: {duration:.3f} ч.;"
        "Дистанция: {distance:.3f} км;"
        "Ср.скорость: {speed:.3f} км / ч;"
        "Потрачено ккал: {calories:.3f}."
    )

    def get_message(self) -> str:
        """Возвращает строку сообщения о тренировке"""
        return self.MESSAGE.format(**asdict(self))


class Training:
    """Базовый класс тренировки."""

    LEN_STEP: float = 0.65
    M_IN_KM: int = 1000
    MIN_IN_HOUR: int = 60

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float) -> None:
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
        return InfoMessage(
            self.__class__.__name__,
            self.duration,
            self.get_distance(),
            self.get_mean_speed(),
            self.get_spent_calories()
        )


class Running(Training):
    """Тренировка: бег."""

    COEFF_CALORIE_1: float = 18
    COEFF_CALORIE_2: float = 20

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        spent_calories = (
            (
                self.COEFF_CALORIE_1
                * self.get_mean_speed()
                - self.COEFF_CALORIE_2
            )
            * self.weight / self.M_IN_KM
            * self.duration * self.MIN_IN_HOUR
        )
        return spent_calories


class SportsWalking(Training):
    """Тренировка: спортивная ходьба."""

    COEFF_WEIGHT_1 = 0.035
    COEFF_WEIGHT_2 = 0.029

    def __init__(self, action: int, duration: float,
                 weight: float, height: float) -> None:
        super().__init__(action, duration, weight)
        self.height = height

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""

        sw_calories = (
            (
                self.COEFF_WEIGHT_1 * self.weight
                + (self.get_mean_speed()**2 // self.height)
                * self.COEFF_WEIGHT_2 * self.weight)
            * self.duration * self.MIN_IN_HOUR
        )
        return sw_calories


class Swimming(Training):
    """Тренировка: плавание."""

    LEN_STEP: float = 1.38
    CALORIES_MEAN_SPEED_MULTIPL: float = 1.1
    COEFF_DOUBL: int = 2

    def __init__(self, action: int, duration: float,
                 weight: float, length_pool: float,
                 count_pool: float) -> None:
        super().__init__(action, duration, weight)
        self.length_pool = length_pool
        self.count_pool = count_pool

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""

        mean_spead = (
            self.length_pool * self.count_pool
            / self.M_IN_KM / self.duration
        )
        return mean_spead

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""

        calories = (
            (self.get_mean_speed()
             + self.CALORIES_MEAN_SPEED_MULTIPL)
            * self.COEFF_DOUBL * self.weight
        )
        return calories


def read_package(workout_type: str, data: List) -> Training:
    """Прочитать данные полученные от датчиков."""

    workout_type_activity: Dict = {
        'SWM': Swimming,
        'RUN': Running,
        'WLK': SportsWalking
    }
    traning = workout_type_activity[workout_type](*data)
    return traning


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
