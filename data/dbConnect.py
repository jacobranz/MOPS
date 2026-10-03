import psycopg2

class dbHelper():
    def __init__(self):
        #db_url = "postgresql://postgres:[password]@db.ebujagqqgpbkvevfuqjl.supabase.co:5432/postgres"
        self.db_url="postgresql://postgres.ebujagqqgpbkvevfuqjl:UoIyrlQRSCjzRtaE@aws-0-us-west-1.pooler.supabase.com:6543/postgres"

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
                RETURNING raid_ID
            """, raidSeason)

            self.raidId = self.cursor.fetchone()[0]

            self.conn.commit()
            return self.raidId

    def addRaidMembers(self, raidMember, raidSeason):
        with self.conn.cursor() as self.cursor:
            self.cursor.execute("""
                INSERT INTO raid_members (
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
                RETURNING raid_member_id
            """, {
                **raidMember,
                "raidID": raidSeason
            })

            self.raidMemberId = self.cursor.fetchone()[0]

            self.conn.commit()
            return self.raidMemberId

    def addRaidLogs(self, raidLog, raidID):
        with self.conn.cursor() as self.cursor:
            self.cursor.execute("""
                INSERT INTO raid_logs (
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
                    %(raidId)s.
                    %(logType)s,
                    %(clanTag)s,
                    %(clanName)s,
                    %(clanLevel)s,
                    %(attackCount)s,
                    %(districtCount)s,
                    %(districtsDestroyed)s
                )
                RETURNING raid_log_id
            """, {
                **raidLog,
                "raidID": raidID
            })

            self.raidLogId = self.cursor.fetchone()[0]

            self.conn.commit()
            return self.raidLogId

    def addRaidDistricts(self, raidDistrict, raidLogID):
        with self.conn.cursor() as self.cursor:
            self.cursor.execute("""
                INSERT INTO raid_districts (
                    raid_log_id,
                    district_id,
                    district_name,
                    district_hall_level,
                    stars,
                    destruction_percent,
                    attack_count,
                    total_loot
                )
                VALUES (
                    %(raidLogId)s,
                    %(districtID)s,
                    %(districtName)s,
                    %(districtHallLevel)s,
                    %(stars)s,
                    %(destructionPercentage)s,
                    %(attackCount)s,
                    %(totalLoot)s
                )
                RETURNING raid_district_id
            """, {
                **raidDistrict,
                "raidLogId": raidLogID
            })

            self.raidDistrictId = self.cursor.fetchone()[0]

            self.conn.commit()
            return self.raidDistrictId

    def addRaidAttacks(self, raidAttack, raidDistrictID):
        with self.conn.cursor() as self.cursor:
            self.cursor.execute("""
                INSERT INTO raid_attacks (
                    raid_district_id,
                    attacker_tag,
                    attacker_name,
                    destruction_percent,
                    stars
                )
                VALUES (
                    %(raidDistrictId)s,
                    %(attackerTag)s,
                    %(attackerName)s,
                    %(destrPercent)s,
                    %(stars)s
                )
            """, {
                **raidAttack,
                "raidDistrictId": raidDistrictID
            })

            self.conn.commit()