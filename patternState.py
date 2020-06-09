'''Эмулятор контрольно-кассовой машины'''
from __future__ import annotations
from abc import ABC, abstractclassmethod

class State(ABC):
    """Интерфейс состояния"""

    def __init__(self,context: PosEmulator):
        self.context = context

    @abstractclassmethod
    def make_operation(self,operation: str):
        pass

    @abstractclassmethod
    def open_session(self):
        pass

    @abstractclassmethod
    def close_session(self):
        pass

'''реализации состояний'''

class SessionClosedState(State):
    """Состояние закрытой смены"""
    def open_session(self):
        """Открытие смены"""
        print('Открываем смену')
        self.context.state = SessionOpenedState(self.context)

    def close_session(self):
        """Если выполнить команду закрыть смену, то аппарат будет печатать копию отчёта"""
        print('Печатаем копию отчета')

    def make_operation(self,operation: str):
        """При попытке проведения операции выдает ошибку, т.к при закрытой смене нельзя проводить операции"""
        print(f'Выполняем фиксальную операцию: {operation}')
        raise Exception('Смена закрыта. Операция невозможна')

class SessionOpenedState(State):
    """Открытая смена"""
    def open_session(self):
        """При коменде "открыть смену" ничего не произойдет, т.к она уже открыта"""
        pass

    def close_session(self):
        """При команде "закрыть смену" напечатает отчёт и перейдет в состояние закрытой смены"""
        print('Печатаем отчёт')
        self.context.state = SessionClosedState(self.context)

    def make_operation(self,operation: str):
        """При команде "выполнить операцию" успешно её проведет, т.к смена открыта"""
        print(f'Выполняем фиксальную операцию: {operation} - успешно')


class SessionExpiredState(State):
    """Состояние, когда смена превышает 24 часа - проведение операций становится невозможным,
       но смена по-прежнему считается открытой"""
    def open_session(self):
        """При коменда "открыть смену" ничего не произойдет, т.к она и так открыта"""
        pass

    def close_session(self):
        """При команде "закрыть смену" напечатает отчёт и перейдет в состояние закрытой смены"""
        print('Печатаем отчёт')
        self.context.state = SessionClosedState (self.context)

    def make_operation(self,operation: str):
        """При команде "выполнить операцию" произойдет ошибка, т.к операции невозможны в таком состоянии"""
        print(f'Выолняем фискальную операцию {operation}')
        raise Exception('Смена превысила 24 часа. Операция невозможна')

class PosEmulator:
    """Эмулятор, котоырй управляет состояниями"""
    def __init__(self):
        """Начальное состояние - смена закрыта"""
        self.state: State = SessionClosedState(self)

    def open_session(self):
        self.state.open_session()

    def close_session(self):
        self.state.close_session()

    def make_operation(self, operation: str):
        self.state.make_operation(operation)

    def make_session_expired(self):
        self.state = SessionExpiredState(self)

if __name__ == '__main__':
    emulator = PosEmulator()
    try:
        emulator.make_operation('Оплата 2000р')
    except Exception as e:
        print(e)
    emulator.open_session()
    try:
        emulator.make_operation('Оплата 2000р')
    except Exception as e:
        print(e)
    emulator.make_session_expired()
    try:
        emulator.make_operation('Оплата 3000р')
    except Exception as e:
        print(e)
    emulator.close_session()
    emulator.open_session()
    try:
        emulator.make_operation('Оплата 300р')
    except Exception as e:
        print(e)
    emulator.close_session()


