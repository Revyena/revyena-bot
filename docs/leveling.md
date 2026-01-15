# Leveling
The leveling module enhances communication and activity by encouraging users to participate more actively in communities.
Experience is earned by sending messages in channels where the leveling system is enabled. As users accumulate experience,
they progress through levels. Leveling gradually becomes more challenging as new levels require more experience to achieve.

## Database Schema
The leveling system uses the following database schema:
```json
{
  "leveling": {
    "columns": {
      "id": "SERIAL PRIMARY KEY",
      "user_id": "BIGINT  NOT NULL",
      "guild_id": "BIGINT NOT NULL",
      "experience": "BIGINT NOT NULL",
      "created_date": "TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP",
      "updated_date": "TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP"
    },
    "constraints": [
      "PRIMARY KEY (guild_id, user_id)"
    ]
  }
}
```

## Commands
- `/level` - Displays the user's current level and experience

## Internal Logic
Experience is calculated with the following formula:
```python
class LevelingMath:
    BASE_XP = 100       # XP required for level 1
    EXPONENT = 2.5      # higher = slower leveling

    @classmethod
    def total_xp_for_level(cls, level: int) -> int:
        """Total XP required to reach a given level."""
        if level <= 0:
            return 0
        return int(cls.BASE_XP * (level ** cls.EXPONENT))
```

For example, to reach level 2, `100 * (2 ** 2.5) = 565` experience is required,
and to reach level 3, `100 * (3 ** 2.5) = 1,558` experience is required.

When a user sends a message, they earn a random amount of experience between 5 and 30 points.
If the user levels up, the system sends a congratulatory message in the channel the message was sent in.

## Functions

### LevelingMath
- `total_xp_for_level(level: int) -> int`  
  Returns the total XP required to reach `level`. Levels <= 0 return 0.

- `level_from_xp(experience: int) -> int`  
  Converts total XP into the corresponding level. Raises `ValueError` for negative XP.

- `xp_to_next_level(experience: int) -> int`  
  Returns how much XP is required to reach the next level from the given total XP.

### LevelingRepository
All repository methods are `async` and accept a `RevyenaBot` instance as the first parameter.

- `get_experience(bot: RevyenaBot, guild_id: int, user_id: int) -> XPDatabaseRecord | None`  
  Fetches the full `XPDatabaseRecord` for `(guild_id, user_id)`. Returns `None` if no row exists.

- `set_experience(bot: RevyenaBot, guild_id: int, user_id: int, experience: int) -> None`  
  Inserts or updates the user's `experience` using an UPSERT. Updates `updated_date` on conflict.

- `get_leaderboard(bot: RevyenaBot, guild_id: int, limit: int = 10) -> list[XPDatabaseRecord]`  
  Returns the top users in a guild ordered by `experience`.

### LevelingService
- `can_award_xp(user: XPDatabaseRecord, message: discord.Message) -> bool`  
  Checks whether enough time has passed since `user.updated_date` to award XP again. Uses `LevelingService.COOLDOWN_SECONDS` (45 by default). Handles timezone-awareness for `updated_date` and `message.created_at`.

- `apply_xp_on_message(current_xp: int, min_xp: int = 5, max_xp: int = 30) -> XPResult`  
  Applies XP math (random XP between `min_xp` and `max_xp`), returns `XPResult` with `old_xp`, `new_xp`, `old_level`, `new_level`, `leveled_up`, and `xp_gained`. This function does **not** check cooldowns; call `can_award_xp` first when enforcing cooldowns.

### XPResult (dataclass)
- `old_xp: int` — XP before applying
- `new_xp: int` — XP after applying
- `old_level: int` — Level before applying
- `new_level: int` — Level after applying
- `leveled_up: bool` — `True` when `new_level > old_level`
- `xp_gained: int` — Amount of XP added

### XPDatabaseRecord (dataclass)
- `user_id: int`
- `guild_id: int`
- `experience: int`
- `created_date: datetime`
- `updated_date: datetime`

## Known issues
- The leaderboard command formats badly on desktop due to a cv2 linebreak issue.
