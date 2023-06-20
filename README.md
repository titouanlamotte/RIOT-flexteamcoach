# RIOT-flexteamcoach

## ./Discord        Discord Chat Bot & Tasks
Cog list:     extensions = ['admin','lol','tft']

### Admin Cog
- !unload  $            : unloads a cog
- !load    $            : calls the unload command and then the load one for a specific cog
- !clear   $            : deletes $ previous messages in the current chat

### tft Cog
- !TFT                  : display the top rankings for TFT queues

### lol Cog
- !LOL                  : display the top rankings for LOL queues
- !mmr $                : Returns the summoner $ mmr calculated by whatismymmr.com/api
- !lol_count_games      : LoL games played by summoner for all queues
- !lol_count_masteries  : LoL best masteries summed between all palyers 
- !lol_best_masteries   : ChampionPoints by Summoner by Champion
- !lol_XP_masteries     : Masteries XP by Summoner

## ./Discord/Crawler        Riot Games APIs and feeding the DB
### Crawler/.               Generic Config and functions

### Crawler/Bot             Functions for the Discord bot

### Crawler/Job             Functions for cron jobs
