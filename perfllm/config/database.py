from dataclasses import dataclass
from typing import Optional
import dataclasses

@dataclass
class DBConfig:
    """Arguments for Database."""
    datafile: str = None
    enable_token_num: bool = False
    model: Optional[str] = None
    seed: Optional[int] = 0

    @classmethod
    def from_cli_args(cls, args):
        attrs = [attr.name for attr in dataclasses.fields(cls)]
        return cls(**{attr: getattr(args,"db_"+attr) for attr in attrs})

    @classmethod
    def from_json_args(cls, args):
        attrs = [attr.name for attr in dataclasses.fields(cls)]
        return cls(**{attr: args.get("db_"+attr, getattr(cls, attr)) for attr in attrs})
        
    def to_dict(self):
        return dict(
            (field.name, getattr(self, field.name)) for field in dataclasses.fields(self))
    