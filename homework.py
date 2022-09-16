from typing import List, Dict, Type
from typing import ClassVar
from dataclasses import dataclass
from dataclasses import asdict


@dataclass
class InfoMessage:
    """Информационное сообщение о тренировке."""
    training_type: str
    duration: float
    distance: float
    speed: float
    calories: float
    MESSAGE: str = (
        "Тип тренировки: {training_type}; "
        "Длительность: {duration:.3f} ч.; "
        "Дистанция: {distance:.3f} км; "
        "Ср. скорость: {speed:.3f} км/ч; "
        "Потрачено ккал: {calories:.3f}."
    )

    def get_message(self) -> str:
        """Возвращает строку сообщения о тренировке"""
        return self.MESSAGE.format(**asdict(self))


@dataclass
class Training:
    """Базовый класс тренировки."""

    action: int
    duration: float
    weight: float
    LEN_STEP: ClassVar[float] = 0.65
    M_IN_KM: ClassVar[int] = 1000
    MIN_IN_HOUR: ClassVar[int] = 60

    def get_distance(self) -> float:
        """Получить дистанцию в км."""
        return self.action * self.LEN_STEP / self.M_IN_KM

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""
        return self.get_distance() / self.duration

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        raise NotImplementedError

    def show_training_info(self) -> InfoMessage:
        """Вернуть информационное сообщение о выполненной тренировке."""
        return InfoMessage(
            type(self).__name__,
            self.duration,
            self.get_distance(),
            self.get_mean_speed(),
            self.get_spent_calories()
        )


@dataclass
class Running(Training):
    """Тренировка: бег."""

    CALORIES_RUN_GET_MEAN_SPEED_MULTIPLIER: ClassVar[float] = 18
    CALORIES_GET_MEAN_SPEED_SUBTRAHEND: ClassVar[float] = 20

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        spent_calories = (
            (
                self.CALORIES_RUN_GET_MEAN_SPEED_MULTIPLIER
                * self.get_mean_speed()
                - self.CALORIES_GET_MEAN_SPEED_SUBTRAHEND
            )
            * self.weight / self.M_IN_KM
            * self.duration * self.MIN_IN_HOUR
        )
        return spent_calories


@dataclass
class SportsWalking(Training):
    """Тренировка: спортивная ходьба."""

    height: float
    CALORIES_WEIGHT_MULTIPLIER: ClassVar[float] = 0.035
    CALORIES_MULTIPLIER_WEIGHT: ClassVar[float] = 0.029

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""

        sw_calories = (
            (
                self.CALORIES_WEIGHT_MULTIPLIER * self.weight
                + (self.get_mean_speed() ** 2 // self.height)
                * self.CALORIES_MULTIPLIER_WEIGHT * self.weight)
            * self.duration * self.MIN_IN_HOUR
        )
        return sw_calories


@dataclass
class Swimming(Training):
    """Тренировка: плавание."""

    length_pool: float
    count_pool: float
    LEN_STEP: ClassVar[float] = 1.38
    CALORIES_SWIM_MEAN_SPEED_MULTIPL: ClassVar[float] = 1.1
    COEFF_DOUBL: ClassVar[int] = 2

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
             + self.CALORIES_SWIM_MEAN_SPEED_MULTIPL)
            * self.COEFF_DOUBL * self.weight
        )
        return calories


def read_package(workout_type: str, data: List[int]) -> Training:
    """Прочитать данные полученные от датчиков."""

    workout_types: Dict[str, Type] = {
        'SWM': Swimming,
        'RUN': Running,
        'WLK': SportsWalking
    }
    if workout_type not in workout_types:
        raise ValueError(
            ('Входящий пакет данных содержит'
             'не существующий ключ {workout_type}.'
             ' Проверьте правильность передаваемых данных.')
        )
    traning = workout_types[workout_type](*data)
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
