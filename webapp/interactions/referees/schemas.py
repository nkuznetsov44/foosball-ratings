from marshmallow_dataclass import class_schema

from webapp.interactions.referees.entities import Referee


RefereeSchema = class_schema(Referee)
