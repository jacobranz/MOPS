import psycopg2

class dbHelper():
    def __init__(self):
        #db_url = "postgresql://postgres:[password]@db.ebujagqqgpbkvevfuqjl.supabase.co:5432/postgres"
        self.db_url="postgresql://postgres.ebujagqqgpbkvevfuqjl:[password]@aws-0-us-west-1.pooler.supabase.com:6543/postgres"

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
                    INSERT INTO current_wars (
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
                    RETURNING war_id
                    """, currentWar)

                self.warId = self.cursor.fetchone()[0]

                self.conn.commit()
                return self.warId

    def addWarMembers(self, warMembers, warID):
        with self.conn.cursor() as self.cursor:
            self.cursor.execute("""
                INSERT INTO war_members (
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
                RETURNING war_memberid
            """, {
                **warMembers,
                "warID": warID
            })

            self.warMemberId = self.cursor.fetchone()[0]

            self.conn.commit()
            return self.warMemberId

    def addWarAttacks(self, warAttack, warMemberID):
        with self.conn.cursor() as self.cursor:
            self.cursor.execute("""
                INSERT INTO war_attacks (
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
                """, {
                    **warAttack,
                    "warMemberID": warMemberID
                })

        self.conn.commit()

    def addRaidSeasons(self, raidSeason):
        with self.conn.cursor() as self.cursor:
            self.cursor.execute("""
                INSERT INTO raid_seasons (
                    state,
                    raid_start,
                    raid_end,
                    total_loot,
                    raid_count,
                    attack_count,
                    destr_districts,
                    offensive_reward,
                    defensive_reward,
                    total_defense_loot,
                    defense_attack_count,
                    defense_destr_districts
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
                    %(defenseReward)s,
                    %(defenseLoot)s,
                    %(defenseAttacks)s,
                    %(defenseDestrDistrictCount)s
                )
            """, raidSeason)

        self.conn.commit()