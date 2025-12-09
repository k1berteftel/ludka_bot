from dataclasses import dataclass

from environs import Env

'''
    При необходимости конфиг базы данных или других сторонних сервисов
'''


@dataclass
class tg_bot:
    token: str
    admin_ids: list[int]
    chat_id: int


@dataclass
class DB:
    dns: str


@dataclass
class Fragment:
    api_key: str


@dataclass
class Config:
    bot: tg_bot
    db: DB
    fragment: Fragment


def load_config(path: str | None = None) -> Config:
    env: Env = Env()
    env.read_env(path)

    return Config(
        bot=tg_bot(
            token=env('token'),
            admin_ids=list(map(int, env.list('admins'))),
            chat_id=int(env('chat_id'))
        ),
        db=DB(
            dns=env('dns')
        ),
        fragment=Fragment(
            api_key=env('fragment_api_key')
        )
    )
