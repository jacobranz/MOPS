create table if not exists clans (
  clan_ID integer not null generated always as identity,
  primary key (clan_ID)
);

create table if not exists wars (
  war_ID integer not null generated always as identity,
  result varchar(255), 
  end_time date,
  team_size integer,
  clan_tagID varchar(255) not null,
  clan_name varchar(255),
  clan_level integer,
  clan_attacks integer,
  clan_stars integer,
  clan_destructionPer float,
  clan_expEarned integer,
  opponent_tagID varchar(255) not null,
  opponent_name varchar(255),
  opponent_level integer,
  opponent_stars integer,
  opponent_destructionPer float,
  primary key (war_ID)
);

create table if not exists current_wars (
  war_ID int not null generated always as identity,
  team_size int,
  battle_mod varchar(255),
  prep_start date,
  war_start date,
  war_end date,
  clan_tag varchar(15),
  clan_name varchar(40),
  clan_level int,
  clan_attacks int,
  clan_stars int,
  clan_destructionper float,
  opp_tag varchar(15),
  opp_name varchar(40),
  opp_level int,
  opp_attacks int,
  opp_stars int,
  opp_destructionper float,
  primary key (war_ID)
);

create table if not exists war_members (
  war_memberID int not null generated always as identity,
  war_ID int,
  player_tag varchar(15),
  player_name varchar(40),
  player_thLevel int,
  player_mapPos int,
  primary key (war_memberID),
  constraint fk_current_war foreign key (war_ID) references current_wars (war_ID)
);

CREATE TABLE IF NOT EXISTS war_attacks (
    war_attackID int not null GENERATED ALWAYS AS IDENTITY,
    war_memberID int,
    attacker_tag varchar(15),
    defender_tag varchar(15),
    attack_stars int,
    attack_destrPer float,
    attack_order int,
    attack_duration int,

    PRIMARY KEY (war_attackID),

    CONSTRAINT fk_war_member
        FOREIGN KEY (war_memberID)
        REFERENCES war_members (war_memberID)
);

create table if not exists raid_seasons (
  raid_ID int not null generated always as identity,
  state varchar(15),
  raid_start date,
  raid_end date,
  total_loot int,
  raid_count int,
  attack_count int,
  destr_districts int,
  offensive_reward int,
  defensive_reward int,
  total_defense_loot int,
  defense_attack_count int,
  defense_destr_districts int,
  primary key (raid_ID)
);

create table if not exists raid_members (
  raid_member_ID int not null generated always as identity,
  raid_ID int,
  tag varchar(15),
  name varchar(40),
  attacks int,
  attack_limit int,
  bonus_attack_limit int,
  resources_looted int,
  primary key (raid_member_id),
  constraint fk_raid_member
    foreign key (raid_ID)
    references raid_seasons (raid_ID)
);

create table if not exists raid_logs (
  raid_log_ID int not null generated always as identity,
  raid_ID int,
  log_type varchar(15),
  clan_tag varchar(15),
  clan_name varchar(40),
  clan_level int,
  attack_count int,
  district_count int,
  districts_destroyed int,
  primary key (raid_log_ID),
  constraint fk_raid_log
    foreign key (raid_ID)
    references raid_seasons (raid_ID)
);

create table if not exists raid_districts (
  raid_district_ID int not null generated always as identity,
  raid_log_ID int,
  district_ID int,
  district_name varchar(40),
  district_hall_level int,
  stars int,
  destruction_percent float,
  attack_count int,
  total_looted int,
  primary key (raid_district_ID),
  constraint fk_raid_log
    foreign key (raid_log_ID)
    references raid_logs (raid_log_ID)
);

create table if not exists raid_attacks (
  raid_attack_ID int not null generated always as identity,
  raid_district_ID int,
  attacker_tag varchar(15),
  attacker_name varchar(40),
  destruction_percent float,
  stars int,
  primary key (raid_attack_ID),
  constraint fk_district_id
    foreign key (raid_district_ID)
    references raid_districts (raid_district_ID)
);