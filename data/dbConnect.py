import psycopg2
import os
from dotenv import load_dotenv

load_dotenv()

class dbHelper():
    def __init__(self):
        self.db_url = os.getenv("DB_URL")

        self.conn = psycopg2.connect(self.db_url)

    def addWar(self, warData):
        if warData == None:
            return None
        else:
            with self.conn.cursor() as self.cursor:
                self.cursor.execute("""
                    INSERT INTO wars (
                        result,
                        end_time,
                        team_size,
                        clan_tagid,
                        clan_name,
                        clan_level,
                        clan_attacks,
                        clan_stars,
                        clan_destructionper,
                        clan_expearned,
                        opponent_tagid,
                        opponent_name,
                        opponent_level,
                        opponent_stars,
                        opponent_destructionper
                    )
                    VALUES (
                        %(result)s,
                        %(endTime)s,
                        %(teamSize)s,
                        %(clanTag)s,
                        %(clanName)s,
                        %(clanLevel)s,
                        %(clanAttacks)s,
                        %(clanStars)s,
                        %(clanDestrPer)s,
                        %(clanExpEarn)s,
                        %(opponentTag)s,
                        %(opponentName)s,
                        %(opponentLevel)s,
                        %(opponentStars)s,
                        %(opponentDestrPer)s
                    )
                    """, warData)

                self.conn.commit()

    def addCurrentWar(self, currentWar):
        if currentWar == "notInWar":
            return
        else:
            with self.conn.cursor() as self.cursor:
                self.cursor.execute("""
                    INSERT INTO current_wars_test (
                        team_size,
                        battle_mod,
                        prep_start,
                        war_start,
                        war_end,
                        clan_tag,
                        clan_name,
                        clan_level,
                        clan_attacks,
                        clan_stars,
                        clan_destructionper,
                        opp_tag,
                        opp_name,
                        opp_level,
                        opp_attacks,
                        opp_stars,
                        opp_destructionper
                    )
                    VALUES (
                        %(teamSize)s,
                        %(battleMod)s,
                        %(prepStart)s,
                        %(warStart)s,
                        %(warEnd)s,
                        %(clanTag)s,
                        %(clanName)s,
                        %(clanLevel)s,
                        %(clanAttacks)s,
                        %(clanStars)s,
                        %(clanDestrPer)s,
                        %(opponentTag)s,
                        %(opponentName)s,
                        %(opponentLevel)s,
                        %(opponentAttacks)s,
                        %(opponentStars)s,
                        %(opponentDestrPer)s
                    )
                    ON CONFLICT (clan_tag, war_end)
                    DO NOTHING
                    RETURNING war_id
                    """, currentWar)

                self.warId = self.cursor.fetchone()

                self.conn.commit()

                if self.warId:
                    return self.warId[0]

                return None

    def addWarMembers(self, warMembers, warID):
        with self.conn.cursor() as self.cursor:
            self.cursor.execute("""
                INSERT INTO war_members_test (
                    war_id,
                    player_tag,
                    player_name,
                    player_thlevel,
                    player_mappos
                )
                VALUES (
                    %(warID)s,
                    %(playerTag)s,
                    %(playerName)s,
                    %(playerThLevel)s,
                    %(playerMapPos)s
                )
                ON CONFLICT (war_id, player_tag)
                DO NOTHING
                RETURNING war_memberid
            """, {
                **warMembers,
                "warID": warID
            })

            self.warMemberId = self.cursor.fetchone()

            self.conn.commit()

            if self.warMemberId:
                return self.warMemberId[0]

            return None

    def addWarAttacks(self, warAttack, warMemberID):
        with self.conn.cursor() as self.cursor:
            self.cursor.execute("""
                INSERT INTO war_attacks_test (
                    war_memberid,
                    attacker_tag,
                    defender_tag,
                    attack_stars,
                    attack_destrper,
                    attack_order,
                    attack_duration
                )
                VALUES (
                    %(warMemberID)s,
                    %(attackerTag)s,
                    %(defenderTag)s,
                    %(attackStars)s,
                    %(attackDestrPer)s,
                    %(attackOrder)s,
                    %(attackDuration)s
                )
                ON CONFLICT (war_memberid, attack_order)
                DO NOTHING
                """, {
                    **warAttack,
                    "warMemberID": warMemberID
                })

        self.conn.commit()

    def addRaidSeasons(self, raidSeason):
        with self.conn.cursor() as self.cursor:
            self.cursor.execute("""
                INSERT INTO raid_seasons_test (
                    state,
                    raid_start,
                    raid_end,
                    total_loot,
                    raid_count,
                    attack_count,
                    destr_districts,
                    offensive_reward,
                    defensive_reward
                )
                VALUES (
                    %(state)s,
                    %(raidStart)s,
                    %(raidEnd)s,
                    %(totalLoot)s,
                    %(raidCount)s,
                    %(attackCount)s,
                    %(destrDistrictCount)s,
                    %(offenseReward)s,
                    %(defenseReward)s
                )
                ON CONFLICT (raid_start, total_loot, raid_count, attack_count, offensive_reward)
                DO NOTHING
                RETURNING raid_ID
            """, raidSeason)

            self.raidId = self.cursor.fetchone()

            self.conn.commit()

            if self.raidId:
                return self.raidId[0]

            return None

    def addRaidMembers(self, raidMember, raidSeason):
        with self.conn.cursor() as self.cursor:
            self.cursor.execute("""
                INSERT INTO raid_members_test (
                    raid_id,
                    tag,
                    name,
                    attacks,
                    attack_limit,
                    bonus_attack_limit,
                    resources_looted
                )
                VALUES (
                    %(raidID)s,
                    %(tag)s,
                    %(name)s,
                    %(attacks)s,
                    %(attackLimit)s,
                    %(bonusAttackLimit)s,
                    %(resourcesLooted)s
                )
                ON CONFLICT (raid_id, tag, resources_looted)
                DO NOTHING
                RETURNING raid_member_id
            """, {
                **raidMember,
                "raidID": raidSeason
            })

            self.raidMemberId = self.cursor.fetchone()

            self.conn.commit()

            if self.raidMemberId:
                return self.raidMemberId[0]

            return None

    def addRaidLogs(self, raidLog, raidID):
        with self.conn.cursor() as self.cursor:
            self.cursor.execute("""
                INSERT INTO raid_logs_test (
                    raid_id,
                    log_type,
                    clan_tag,
                    clan_name,
                    clan_level,
                    attack_count,
                    district_count,
                    districts_destroyed
                )
                VALUES (
                    %(raidID)s,
                    %(logType)s,
                    %(clanTag)s,
                    %(clanName)s,
                    %(clanLevel)s,
                    %(attackCount)s,
                    %(districtCount)s,
                    %(districtsDestroyed)s
                )
                ON CONFLICT (raid_id, log_type, clan_tag, attack_count, district_count)
                DO NOTHING
                RETURNING raid_log_id
            """, {
                **raidLog,
                "raidID": raidID
            })

            self.raidLogId = self.cursor.fetchone()

            self.conn.commit()

            if self.raidLogId:
                return self.raidLogId

            return None

    def addRaidDistricts(self, raidDistrict, raidLogID):
        with self.conn.cursor() as self.cursor:
            self.cursor.execute("""
                INSERT INTO raid_districts_test (
                    raid_log_id,
                    district_id,
                    district_name,
                    district_hall_level,
                    stars,
                    destruction_percent,
                    attack_count,
                    total_looted
                )
                VALUES (
                    %(raidLogId)s,
                    %(districtID)s,
                    %(districtName)s,
                    %(districtHallLevel)s,
                    %(stars)s,
                    %(destructionPercentage)s,
                    %(attackCount)s,
                    %(totalLooted)s
                )
                ON CONFLICT (raid_log_id, district_id, attack_count, total_looted)
                DO NOTHING
                RETURNING raid_district_id
            """, {
                **raidDistrict,
                "raidLogId": raidLogID
            })

            self.raidDistrictId = self.cursor.fetchone()

            self.conn.commit()

            if self.raidDistrictId:
                return self.raidDistrictId

            return None

    def addRaidAttacks(self, raidAttack, raidDistrictID):
        with self.conn.cursor() as self.cursor:
            self.cursor.execute("""
                INSERT INTO raid_attacks_test (
                    raid_district_id,
                    tag,
                    name,
                    destruction_percent,
                    stars
                )
                VALUES (
                    %(raidDistrictId)s,
                    %(tag)s,
                    %(name)s,
                    %(destrPercent)s,
                    %(stars)s
                )
            """, {
                **raidAttack,
                "raidDistrictId": raidDistrictID
            })

            self.conn.commit()

    def getWarDestrOvertime(self):
        with self.conn.cursor() as self.cursor:
            self.cursor.execute("""
                SELECT 
                    end_time, 
                    clan_name,
                    clan_attacks,
                    clan_stars,
                    opponent_name,
                    opponent_stars,
                    opponent_destructionper,
                    clan_destructionper 
                FROM wars
                WHERE clan_name = 'Panda Supreme'
                ORDER BY end_time;
            """)

            return self.cursor.fetchall()

    def getPlayerDestruction(self):
        with self.conn.cursor() as self.cursor:
            self.cursor.execute("""
                SELECT 
                    wm.player_name,
                    wa.attack_destrper
                FROM war_attacks wa
                JOIN war_members wm
                    ON wa.war_memberid = wm.war_memberid
                WHERE wa.attack_destrper IS NOT NULL
                ORDER BY wm.player_name;
            """)

            return self.cursor.fetchall()

    def getPlayerStars(self):
        with self.conn.cursor() as self.cursor:
            self.cursor.execute("""
                SELECT
                    wm.player_name,
                    wa.attack_stars
                FROM war_attacks wa
                JOIN war_members wm
                    ON wa.war_memberid = wm.war_memberid
                WHERE wa.attack_stars IS NOT NULL
                ORDER BY wm.player_name;
            """)

            return self.cursor.fetchall()

    def getWarParticipation(self):
        with self.conn.cursor() as self.cursor:
            self.cursor.execute("""
                SELECT
                    wm.player_name,
                    wm.war_id
                FROM war_members wm
                ORDER BY wm.player_name, wm.war_id;
            """)

            return self.cursor.fetchall()

    def getAttackEfficiency(self):
        with self.conn.cursor() as self.cursor:
            self.cursor.execute("""
                SELECT
                    war_id,
                    end_time,
                    team_size,
                    clan_attacks,
                    clan_stars,
                    clan_destructionper
                FROM wars
                ORDER BY end_time;
            """)

            return self.cursor.fetchall()