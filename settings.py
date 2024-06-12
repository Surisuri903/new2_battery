from os import environ

SESSION_CONFIGS = [
    dict(
       name='session_1',
       display_name="Battery (Trust/Dictator, Risk from Experience, Kirby Monetary Choices, Tower of London)",
       num_demo_participants=1,
       app_sequence=['consent', 'trust','dictator', 'risk_from_experience_task','kirby_monetary_choices', 'tower_of_london']
    ),
    dict(
        name='session_2',
        display_name="Battery (Centipede, Bart, Hybrid-Delay)",
        num_demo_participants=1,
        app_sequence=['centipede_intro', 'centipede_training', 'centipede_task', 'centipede_results', 'bart', 'hybrid_delay_task'],
        seconds_per_coin_transfer=60,
        rects_per_minute=4,
        small_payoff=4,
        seconds_for_timeout=10
    ),
    dict(
       name='session_3',
       display_name="Battery (Zurich Prosocial Game, Risk from Description, Boat)",
       num_demo_participants=1,
       app_sequence=['zurich_game', 'risk_from_description', 'patience_game_intro', 'patience_game', 'patience_game_results']
    ),
    dict(
        name="trust",
        display_name="Trust",
        num_demo_participants=1,
        app_sequence=['trust']
    ),
    dict(
        name="dictator",
        display_name="Dictator",
        num_demo_participants=1,
        app_sequence=['dictator']
    ),
    dict(
        name="risk_from_experience",
        display_name="Risk From Experience",
        num_demo_participants=1,
        app_sequence=['risk_from_experience_task']
    ),
    dict(
        name="kirby_monetary_choices",
        display_name="Kirby Monetary Choices",
        num_demo_participants=1,
        app_sequence=['kirby_monetary_choices']
    ),
    dict(
        name="tower_of_london",
        display_name="Tower of London",
        num_demo_participants=1,
        app_sequence=['tower_of_london']
    ),
    dict(
        name="centipede",
        display_name="Centipede",
        num_demo_participants=1,
        app_sequence=['centipede_intro', 'centipede_training', 'centipede_task', 'centipede_results']
    ),
    dict(
        name="bart",
        display_name="Bart",
        num_demo_participants=1,
        app_sequence=['bart']
    ),
    dict(
        name="hybrid_delay_task",
        display_name="Hybrid Delay Task",
        num_demo_participants=1,
        app_sequence=['hybrid_delay_task'],
        seconds_per_coin_transfer=60,
        rects_per_minute=4,
        small_payoff=4,
        seconds_for_timeout=10
    ),
    dict(
        name="zurich",
        display_name="Zurich Game",
        num_demo_participants=1,
        app_sequence=['zurich_game']
    ),    
    dict(
        name="risk_from_description",
        display_name="Risk from Description",
        num_demo_participants=1,
        app_sequence=['risk_from_description']
    ),
    dict(
        name="patience",
        display_name="Patience Game",
        num_demo_participants=1,
        app_sequence=['patience_game_intro', 'patience_game', 'patience_game_results']
    ),
]

# if you set a property in SESSION_CONFIG_DEFAULTS, it will be inherited by all configs
# in SESSION_CONFIGS, except those that explicitly override it.
# the session config can be accessed from methods in your apps as self.session.config,
# e.g. self.session.config['participation_fee']

SESSION_CONFIG_DEFAULTS = dict(
    real_world_currency_per_point=1.00, participation_fee=0.00, doc="",
    num_stones=4,
    num_trees=4,
    sec_per_trial=60,
    kill_time_when_blocked=8,
    use_fixed_falling_door_interval=True,
    falling_door_interval=5,
    sec_for_alter_to_open_door=2,
    sec_for_alter_to_help=2,
    sec_interval_ego_step=1,
    sec_interval_alter_step=1.5,
)

# ISO-639 code
# for example: de, fr, ja, ko, zh-hans
LANGUAGE_CODE = 'he'

# e.g. EUR, GBP, CNY, JPY
# e.g. EUR, GBP, CNY, JPY
REAL_WORLD_CURRENCY_CODE = 'GBP'
USE_POINTS = False

ROOMS = [
    dict(
        name='online',
        display_name='Online'
    )
]

ADMIN_USERNAME = 'admin'
# for security, best to set admin password in an environment variable
ADMIN_PASSWORD = environ.get('OTREE_ADMIN_PASSWORD')

DEMO_PAGE_INTRO_HTML = """ """

SECRET_KEY = '6(sm61d=+t5)(+tqiw17wbc0bhp8ji=d)_fd4!lc#jlr(t_$^='

# if an app is included in SESSION_CONFIGS, you don't need to list it here
INSTALLED_APPS = [
    'otree', 'trust','dictator', 'kirby_monetary_choices', 'risk_from_description', 'risk_from_experience_task', 'zurich_game', 'patience_game_intro', 'patience_game', 'patience_game_results',
    'tower_of_london', 'bart', 'hybrid_delay_task', 'centipede_intro', 'centipede_training', 'centipede_task', 'centipede_results', 'django_user_agents'
]

MIDDLEWARE = (
    # other middlewares...
    'django_user_agents.middleware.UserAgentMiddleware',
)

