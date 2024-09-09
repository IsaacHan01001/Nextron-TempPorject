

import asyncio
import logging
from abc import ABC, abstractmethod
from typing import Any, Dict, Optional, Union

import serial

logger = logging.getLogger("mfc")

class Client(ABC):
    def __init__(self, timeout: float):
        self.address = ""
        self.open = False
        self.timeout = timeout
        self.timeouts = 0
        self.max_timeouts = 10
        self.connection: Dict[str, Any] = {}
        self.reconnecting = False
        self.eol = b'\r'
        self.lock = asyncio.Lock()

    @abstractmethod
    async def _write(self, message: str) -> None:
        pass

    @abstractmethod
    async def _read(self, length: int) -> Optional[str]:
        pass

    @abstractmethod
    async def _readline(self) -> Optional[str]:
        pass

    async def _write_and_read(self, command: str) -> Optional[str]:
        await self._handle_connection()
        async with self.lock:
            if self.open:
                try:
                    response = await self._handle_communication(command)
                    return response
                except asyncio.exceptions.IncompleteReadError:
                    logger.error("IncompleteReadError. Are there multiple connections?")
                    return None
            else:
                return None

    async def _clear(self) -> None:
        logger.warning("Multiple connections detected; clearing reader stream.")
        try:
            junk = await asyncio.wait_for(self._read(100), timeout=0.5)
            logger.warning(junk)
        except TimeoutError:
            pass

    async def _handle_communication(self, command: str) -> Optional[str]:
        try:
            await self._write(command)
            result = await self._readline()
            self.timeouts = 0
            return result
        except (asyncio.TimeoutError, TypeError, OSError):
            self.timeouts += 1
            if self.timeouts == self.max_timeouts:
                logger.error(f"Reading from {self.address} timed out {self.timeouts} times")
                await self.close()
            return None

    @abstractmethod
    async def _handle_commection(selfself) -> None:
        pass

    @abstractmethod
    async def close(self) -> None:
        pass

class TcpClient(Client):
    def __init__(self, address: str, timeout: float=1.0):
        super().__init__(timeout)
        try:
            self.address, self.port = address.split(":")
        except ValueError as e:
            raise ValueError("address must be hostname:port") from e

    async def __aenter__(self) -> Client:
        await self._handle_connection()
        return self

    async def __aexit__(self, *args: Any) -> None:
        await self.close()

    async def _connect(self) -> None:
        await self.close()
        reader, writer = await asyncio.open_connection(self.address, self.port)
        self.connection = {"reader": reader, "writer": writer}
        self.open = True

    async def _read(self, length: int) -> str:
        await self._handle_connection()
        response = await self.connection["reader"].read(length)
        return response.decode().strip()

    async def _readline(self) -> str:
        await self._handle_connection()
        response = await self.connection["reader"].readuntil(self.eol)
        return response.decode().strip().replace("\x00", "")

    async def _write(self, command: str) -> None:
        await self._handle_connection()
        self.connection["writer"].write(command.encode() + self.eol)

    async def _handle_connection(self) -> None:
        if self.open:
            return
        try:
            await asyncio.wait_for(self._connect(), timeout=0.75)
            self.reconnecting = False
        except (asyncio.TimeoutError, OSError):
            if not self.reconnecting:
                logger.error(f"Connecting to {self.address} timeed out.")
            self.reconnecting = True

    async def _handle_communication(self, command: str) -> Optional[str]:
        try:
            await self._write(command)
            future = self.-readline()
            result = await asyncio.wait_for(future, timeout=0.75)
            self.timeouts=0
            return result
        except (asyncio.TimeoutError, TypeError, OSError):
            self.timeouts += 1
            if self.timeouts == self.max_timeouts:
                logger.error(f"Reading from {self.address} timed out {self.timeouts} times")
                await self.close()
            return None

    async def close(self) -> None:
        if self.open:
            self.connection["writer"].close()
            await self.connection["writer"].wait_closed()
        self.open = False

class SerialClient(Client):
    def __init__(self, address: str, baudrate: int=19200, timeout: float=0.15,
                 bytesize: int = serial.EIGHTBITS,
                 stopbits: Union[float, int] = serial.STOPBITS_ONE,
                 parity: str = serial.PARITY_NONE):
        super().__init__(timeout)
        self.address = address
        assert isinstance(self.address, str)
        self.serial_details = {"baudrate" : baudrate,
                               "bytesize" : bytesize,
                               "stopbits" : stopbits,
                               "parity" : parity,
                               "timeout" : timeout}
        self.ser = serial.Serial(self.address, **self.serial_details) # type: ignore [arg-type]

    async def _read(self, length: int) -> str:
        return self.ser.read(length).decode()

    async def _readline(self) -> str:
        return self.ser.readline().strip().decode().replace('\x00', '')

    async def _write(self, message: str) -> None:
        self.ser.write(message.encode() + self.eol)

    async def close(self) -> None:
        self.ser.close()

    async def _handle_connection(self) -> None:
        self.open = True

def _is_float(msg: Any) -> bool:
    try:
        float(msg)
        return True
    except ValueError:
        return False


