import logging
from fastapi import Depends
from typing import Any, List

from fastapi import APIRouter
from fastapi_sqlalchemy import db
from sqlalchemy import desc, asc
from sqlalchemy.orm import aliased

from app.models.team import Team
from app.schema.team import TeamRequest, TeamResponse
from app.schema.base import ResponseSchemaBase
from app.utils.paging import PaginationParams, paginate, Page

router = APIRouter()

logger = logging.getLogger()


@router.get("/", response_model=Page[TeamResponse])
def get_teams(params: PaginationParams = Depends()) -> Any:
    try:
        result = paginate(db.session.query(Team), params)
        return result
    except Exception as e:
        logger.info("error happen")
        logger.error(e)


@router.get("/{team_id}", response_model=TeamResponse)
def get_team(team_id: int):
    try:
        return db.session.query(Team).filter_by(id=team_id).first()
    except Exception as e:
        logger.info(e)


@router.post("/", response_model=TeamResponse)
def create_team(team: TeamRequest):
    try:
        team_db = Team(
            name=team.name,
            code=team.code,
            type=team.type,
            description=team.description
        )
        db.session.add(team_db)
        db.session.commit()
        return team_db
    except Exception as e:
        logger.info(e)


@router.put("/{team_id}", response_model=TeamResponse)
def update_team(team_id: int, team: TeamRequest):
    try:
        team_db = db.session.query(Team).filter_by(id=team_id).first()
        if not team_db:
            return None

        team_db.name = team.name
        team_db.code = team.code
        team_db.type = team.type
        team_db.description = team.description

        db.session.commit()
        return team_db
    except Exception as e:
        logger.info(e)
