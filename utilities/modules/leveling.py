import random
from dataclasses import dataclass
from datetime import datetime, timezone

import discord

from revyenaBot import RevyenaBot


# -----------------------------
# Math utilities
# -----------------------------
class LevelingMath:
    BASE_XP = 100       # XP required for level 1
    EXPONENT = 2.5      # higher = slower leveling

    @classmethod
    def total_xp_for_level(cls, level: int) -> int:
        """Total XP required to reach a given level."""
        if level <= 0:
            return 0
        return int(cls.BASE_XP * (level ** cls.EXPONENT))

    @classmethod
    def level_from_xp(cls, experience: int) -> int:
        """Calculate level based on total XP."""
        if experience < 0:
            raise ValueError("XP must be non-negative")
        return int((experience / cls.BASE_XP) ** (1 / cls.EXPONENT))

    @classmethod
    def xp_to_next_level(cls, experience: int) -> int:
        """XP required to reach the next level."""
        current_level = cls.level_from_xp(experience)
        return cls.total_xp_for_level(current_level + 1) - experience


# -----------------------------
# Dataclass for XP results
# -----------------------------
@dataclass(slots=True)
class XPResult:
    old_xp: int
    new_xp: int
    old_level: int
    new_level: int
    leveled_up: bool
    xp_gained: int

@dataclass(slots=True)
class XPDatabaseRecord:
    user_id: int
    guild_id: int
    experience: int
    created_date: datetime
    updated_date: datetime

# -----------------------------
# Database repository
# -----------------------------
class LevelingRepository:
    @staticmethod
    async def get_experience(bot: RevyenaBot, guild_id: int, user_id: int) -> XPDatabaseRecord | None:
        row = await bot.revhandler.fetchrow(
            'SELECT * FROM leveling WHERE guild_id = $1 AND user_id = $2',
            guild_id,
            user_id
        )

        return XPDatabaseRecord(**dict(row)) if row else None

    @staticmethod
    async def set_experience(bot: RevyenaBot, guild_id: int, user_id: int, experience: int):
        await bot.revhandler.execute(
            '''
            INSERT INTO leveling (guild_id, user_id, experience)
            VALUES ($1, $2, $3)
            ON CONFLICT (guild_id, user_id)
            DO UPDATE SET experience = EXCLUDED.experience, updated_date = CURRENT_TIMESTAMP
            ''',
            guild_id,
            user_id,
            experience
        )

    @staticmethod
    async def get_leaderboard(bot: RevyenaBot, guild_id: int, limit: int = 10) -> list[XPDatabaseRecord]:
        rows = await bot.revhandler.fetch(
            '''
            SELECT * FROM leveling
            WHERE guild_id = $1
            ORDER BY experience DESC
            LIMIT $2
            ''',
            guild_id,
            limit
        )

        return [XPDatabaseRecord(**dict(row)) for row in rows]


# -----------------------------
# Service for handling XP and leveling
# -----------------------------
class LevelingService:
    COOLDOWN_SECONDS = 45

    from datetime import timezone

    @classmethod
    def can_award_xp(cls, user: XPDatabaseRecord, message: discord.Message) -> bool:
        """Check if enough time has passed to award XP again."""

        # Convert updated_date to datetime if it is a string
        last_update = user.updated_date
        if isinstance(last_update, str):
            last_update = datetime.fromisoformat(last_update)

        # Ensure both are UTC-aware
        if last_update.tzinfo is None:
            last_update = last_update.replace(tzinfo=timezone.utc)

        message_time = message.created_at
        if message_time.tzinfo is None:
            message_time = message_time.replace(tzinfo=timezone.utc)

        # Check cooldown
        if (message_time - last_update).total_seconds() <= cls.COOLDOWN_SECONDS:
            return False

        return True

    @staticmethod
    def apply_xp_on_message(
        current_xp: int,
        min_xp: int = 5,
        max_xp: int = 30,
    ) -> XPResult:
        """Apply XP if eligible and return a structured result."""

        old_level = LevelingMath.level_from_xp(current_xp)

        xp_gained = random.randint(min_xp, max_xp)
        new_xp = current_xp + xp_gained
        new_level = LevelingMath.level_from_xp(new_xp)

        return XPResult(
            old_xp=current_xp,
            new_xp=new_xp,
            old_level=old_level,
            new_level=new_level,
            leveled_up=new_level > old_level,
            xp_gained=xp_gained,
        )
