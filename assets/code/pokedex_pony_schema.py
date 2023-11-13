from pony import orm

class Language(db.Entity):
    """A language the Pokémon games have been translated into."""
    _table_ = 'languages'
    id = orm.PrimaryKey(int)
    iso639 = orm.Required(str)
    iso3166 = orm.Required(str)
    identifier = orm.Required(str)
    official = orm.Required(bool)
    order = orm.Optional(int)
    ability_names = orm.Set("AbilityName")
    ability_prose = orm.Set("AbilityProse")
    ability_flavor_text = orm.Set("AbilityFlavorText")
    berry_firmness_names = orm.Set("BerryFirmnessName")
    contest_type_names = orm.Set("ContestTypeName")
    generation_names = orm.Set("GenerationName")
    item_names = orm.Set("ItemName")
    item_prose = orm.Set("ItemProse")
    item_flavor_summaries = orm.Set("ItemFlavorSummary")
    item_category_prose = orm.Set("ItemCategoryProse")
    item_flag_prose = orm.Set("ItemFlagProse")
    item_flavor_texts = orm.Set("ItemFlavorText")
    item_fling_effect_prose = orm.Set("ItemFlingEffectProse")
    item_pocket_names = orm.Set("ItemPocketName")
    names = orm.Set("LanguageName", reverse="language_id")
    names_in_language = orm.Set("LanguageName", reverse="local_language_id")
    region_names = orm.Set("RegionName")
    type_names = orm.Set("TypeName")

class Ability(db.Entity):
    """An ability a Pokémon can have, such as Static or Pressure.

    IDs below 10000 match the internal ID in the games.
    IDs above 10000 are reserved for Conquest-only abilities.
    """
    _table_ = 'abilities'
    id = orm.PrimaryKey(int)
    identifier = orm.Required(str)
    generation_id = orm.Required("Generation")
    is_main_series = orm.Required(bool)
    names = orm.Set("AbilityName")
    prose = orm.Set("AbilityProse")
    # changelog = orm.Set("AbilityChangelog")
    flavor_text = orm.Set("AbilityFlavorText")

class AbilityName(db.Entity):
    _table_ = 'ability_names'
    ability_id = orm.Required(Ability)
    local_language_id = orm.Required(Language)
    name = orm.Required(str)
    orm.PrimaryKey(ability_id, local_language_id)

class AbilityProse(db.Entity):
    _table_ = "ability_prose"
    ability_id = orm.Required(Ability)
    local_language_id = orm.Required(Language)
    short_effect = orm.Optional(str)
    effect = orm.Optional(str)
    orm.PrimaryKey(ability_id, local_language_id)

# class AbilityChangelog(db.Entity):
#     """History of changes to abilities across main game versions."""
#     _table_ = 'ability_changelog'
#     id = orm.PrimaryKey(int)
#     ability_id = orm.Required('abilities.id')
#     changed_in_version_group_id = orm.Required('version_groups.id')

# class AbilityChangelogProse(db.Entity):
#     ability_changelog_id = orm.Required(AbilityChangelog)
#     local_language_id = orm.Required(Language)
#     effect = orm.Required(str)
#     orm.PrimaryKey(ability_changelog_id, local_language_id)

class AbilityFlavorText(db.Entity):
    """In-game flavor text of an ability."""
    _table_ = 'ability_flavor_text'
    ability_id = orm.Required(Ability)
    language_id = orm.Required(Language)
    version_group_id = orm.Required("VersionGroup")
    flavor_text = orm.Required(str)
    orm.PrimaryKey(ability_id, language_id, version_group_id)

class Berry(db.Entity):
    """A Berry, consumable item that grows on trees.

    For data common to all items, such as the name, see the corresponding item entry.

    ID matches the in-game berry number.
    """
    _table_ = 'berries'
    id = orm.PrimaryKey(int)
    item_id = orm.Required("Item")
    firmness_id = orm.Required("BerryFirmness")
    natural_gift_power = orm.Optional(int)
    natural_gift_type_id = orm.Optional("Type")
    size = orm.Required(int)
    max_harvest = orm.Required(int)
    growth_time = orm.Required(int)
    soil_dryness = orm.Required(int)
    smoothness = orm.Required(int)
    flavor = orm.Set("BerryFlavor")

class BerryFirmness(db.Entity):
    """A Berry firmness, such as "hard" or "very soft". """
    _table_ = 'berry_firmness'
    id = orm.PrimaryKey(int)
    identifier = orm.Required(str)
    berries = orm.Set(Berry)
    names = orm.Set("BerryFirmnessName")

class BerryFirmnessName(db.Entity):
    _table_ = "berry_firmness_names"
    berry_firmness_id = orm.Required(BerryFirmness)
    local_language_id = orm.Required(Language)
    name = orm.Required(str)
    orm.PrimaryKey(berry_firmness_id, local_language_id)

class BerryFlavor(db.Entity):
    """A Berry flavor level."""
    _table_ = 'berry_flavors'
    berry_id = orm.Required(Berry)
    contest_type_id = orm.Required("ContestType")
    flavor = orm.Required(int)
    orm.PrimaryKey(berry_id, contest_type_id)

class ContestType(db.Entity):
    """A Contest type, such as "cool" or "smart", and their associated Berry flavors and Pokéblock colors.
    """
    _table_ = 'contest_types'
    id = orm.PrimaryKey(int)
    identifier = orm.Required(str)
    berry_flavors = orm.Set(BerryFlavor)
    names = orm.Set("ContestTypeName")

class ContestTypeName(db.Entity):
    _table_ = "contest_type_names"
    contest_type_id = orm.Required(ContestType)
    local_language_id = orm.Required(Language)
    name = orm.Optional(str)
    flavor = orm.Optional(str)
    color = orm.Optional(str)
    orm.PrimaryKey(contest_type_id, local_language_id)

class Generation(db.Entity):
    """A Generation of the Pokémon franchise."""
    _table_ = 'generations'
    id = orm.PrimaryKey(int)
    main_region_id = orm.Required("Region")
    identifier = orm.Required(str)
    abilities = orm.Set(Ability)
    version_groups = orm.Set("VersionGroup")
    names = orm.Set("GenerationName", reverse="generation_id")
    item_game_indices = orm.Set("ItemGameIndex")
    types = orm.Set("Type")
    type_game_indices = orm.Set("TypeGameIndex")

class GenerationName(db.Entity):
    _table_ = "generation_names"
    generation_id = orm.Required(Generation)
    local_language_id = orm.Required(Language)
    name = orm.Required(str)
    orm.PrimaryKey(generation_id, local_language_id)

class Item(db.Entity):
    """An Item from the games, like "Poké Ball" or "Bicycle".

    IDs do not mean anything; see ItemGameIndex for the IDs used in the games.
    """
    _table_ = 'items'
    id = orm.PrimaryKey(int)
    identifier = orm.Required(str)
    category_id = orm.Required("ItemCategory")
    cost = orm.Required(int)
    fling_power = orm.Optional(int)
    fling_effect_id = orm.Optional("ItemFlingEffect")
    berry = orm.Optional(Berry)
    names = orm.Set("ItemName")
    prose = orm.Set("ItemProse")
    flavor_summaries = orm.Set("ItemFlavorSummary")
    flags = orm.Set("ItemFlag", table="item_flag_map", column="item_id")
    flavor_texts = orm.Set("ItemFlavorText")
    game_indices = orm.Set("ItemGameIndex")
    # @property
    # def appears_underground(self):
    #     """True if the item appears underground, as specified by the appropriate flag."""
    #     return any(flag.identifier == u'underground' for flag in self.flags)

class ItemName(db.Entity):
    _table_ = "item_names"
    item_id = orm.Required(Item)
    local_language_id = orm.Required(Language)
    name = orm.Required(str)
    orm.PrimaryKey(item_id, local_language_id)

class ItemProse(db.Entity):
    _table_ = "item_prose"
    item_id = orm.Required(Item)
    local_language_id = orm.Required(Language)
    short_effect = orm.Optional(str)
    effect = orm.Optional(str)
    orm.PrimaryKey(item_id, local_language_id)

class ItemFlavorSummary(db.Entity):
    _table_ = "item_flavor_summaries"
    item_id = orm.Required(Item)
    local_language_id = orm.Required(Language)
    flavor_summary = orm.Optional(str)
    orm.PrimaryKey(item_id, local_language_id)

class ItemCategory(db.Entity):
    """An item category.  Not official."""
    _table_ = 'item_categories'
    id = orm.PrimaryKey(int)
    pocket_id = orm.Required("ItemPocket")
    identifier = orm.Required(str)
    prose = orm.Set("ItemCategoryProse")
    items = orm.Set(Item)

class ItemCategoryProse(db.Entity):
    _table_ = "item_category_prose"
    item_category_id = orm.Required(ItemCategory)
    local_language_id = orm.Required(Language)
    name = orm.Required(str)
    orm.PrimaryKey(item_category_id, local_language_id)

class ItemFlag(db.Entity):
    """An item attribute such as "consumable" or "holdable".  Not official. """
    _table_ = 'item_flags'
    id = orm.PrimaryKey(int)
    identifier = orm.Required(str)
    prose = orm.Set("ItemFlagProse")
    items = orm.Set("Item", table="item_flag_map", column="item_flag_id")

class ItemFlagProse(db.Entity):
    _table_ = "item_flag_prose"
    item_flag_id = orm.Required(ItemFlag)
    local_language_id = orm.Required(Language)
    name = orm.Optional(str)
    description = orm.Optional(str)
    orm.PrimaryKey(item_flag_id, local_language_id)

class ItemFlavorText(db.Entity):
    """An in-game description of an item."""
    _table_ = 'item_flavor_text'
    # summary_column = Item.flavor_summaries_table, 'flavor_summary'
    item_id = orm.Required(Item)
    version_group_id = orm.Required("VersionGroup")
    language_id = orm.Required(Language)
    flavor_text = orm.Required(str)
    orm.PrimaryKey(item_id, version_group_id, language_id)

class ItemFlingEffect(db.Entity):
    """An effect of the move Fling when used with a specific item."""
    _table_ = 'item_fling_effects'
    id = orm.PrimaryKey(int)
    identifier = orm.Required(str)
    prose = orm.Set("ItemFlingEffectProse")
    item = orm.Set(Item)

class ItemFlingEffectProse(db.Entity):
    _table_ = "item_fling_effect_prose"
    item_fling_effect_id = orm.Required(ItemFlingEffect)
    local_language_id = orm.Required(Language)
    effect = orm.Required(str)
    orm.PrimaryKey(item_fling_effect_id, local_language_id)

class ItemGameIndex(db.Entity):
    """The internal ID number a game uses for an item."""
    _table_ = 'item_game_indices'
    item_id = orm.Required(Item)
    generation_id = orm.Required(Generation)
    game_index = orm.Required(int)
    orm.PrimaryKey(item_id, generation_id)

class ItemPocket(db.Entity):
    """A pocket that categorizes items.  Semi-offical."""
    _table_ = 'item_pockets'
    id = orm.PrimaryKey(int)
    identifier = orm.Required(str)
    names = orm.Set("ItemPocketName")
    categories = orm.Set(ItemCategory)

class ItemPocketName(db.Entity):
    _table_ = "item_pocket_names"
    item_pocket_id = orm.Required(ItemPocket)
    local_language_id = orm.Required(Language)
    name = orm.Required(str)
    orm.PrimaryKey(item_pocket_id, local_language_id)

class LanguageName(db.Entity):
    _table_ = "language_names"
    language_id = orm.Required(Language)
    local_language_id = orm.Required(Language)
    name = orm.Required(str)
    orm.PrimaryKey(language_id, local_language_id)

class Pokemon(db.Entity):
    """A Pokémon.  The core to this whole mess.

    This table defines "Pokémon" the same way the games do: a form with
    different types, moves, or other game-changing properties counts as a
    different Pokémon.  For example, this table contains four rows for Deoxys,
    but only one for Unown.

    Non-default forms have IDs above 10000.
    IDs below 10000 match the species_id column, for convenience.
    """
    _table_ = 'pokemon'
    id = orm.PrimaryKey(int)
    identifier = orm.Required(str)
    species_id = Column(Integer, ForeignKey('pokemon_species.id'),
    height = orm.Required(int)
    weight = orm.Required(int)
    base_experience = orm.Required(int)
    order = orm.Required(int),
    is_default = orm.Required(bool)

    @property
    def name(self):
        """Returns a name for this Pokémon, specifying the form iff it
        represents a specific PokemonForm.
        """
        if any(not form.is_default for form in self.forms):
            return self.species.name
        else:
            return self.default_form.pokemon_name or self.species.name

    def stat(self, stat_identifier):
        """Returns a PokemonStat record for the given stat name (or Stat row
        object).  Uses the normal has-many machinery, so all the stats are
        effectively cached.
        """
        if isinstance(stat_identifier, Stat):
            stat_identifier = stat_identifier.identifier

        for pokemon_stat in self.stats:
            if pokemon_stat.stat.identifier == stat_identifier:
                return pokemon_stat

        raise KeyError(u'No stat named %s' % stat_identifier)

    def base_stat(self, stat_identifier, default=0):
        """Return this Pokemon's base stat value for the given stat identifier,
        or default if missing.
        """

        if isinstance(stat_identifier, Stat):
            stat_identifier = stat_identifier.identifier

        for pokemon_stat in self.stats:
            if pokemon_stat.stat.identifier == stat_identifier:
                return pokemon_stat.base_stat

        return default

    @property
    def better_damage_class(self):
        """Returns the MoveDamageClass that this Pokémon is best suited for,
        based on its attack stats.

        If the attack stats are about equal (within 5), returns None.  The
        value None, not the damage class called 'None'.
        """

        try:
            phys = self.stat(u'attack')
            spec = self.stat(u'special-attack')
        except KeyError:
            return None

        diff = phys.base_stat - spec.base_stat

        if diff > 5:
            return phys.stat.damage_class
        elif diff < -5:
            return spec.stat.damage_class
        else:
            return None

class PokemonAbility(db.Entity):
    """Maps an ability to a Pokémon that can have it."""
    _table_ = 'pokemon_abilities'
    pokemon_id = Column(Integer, ForeignKey('pokemon.id'), primary_key=True, nullable=False, autoincrement=False,

    ability_id = orm.Required('abilities.id')

    # XXX having both a method and a slot is kind of gross.  "slot" is a
    # misnomer, anyway: duplicate abilities don't appear in slot 2.
    # Probably should replace that with "order".
    is_hidden = orm.Required(bool)

    slot = orm.PrimaryKey(int) autoincrement=False,

class Region(db.Entity):
    """Major areas of the world: Kanto, Johto, etc."""
    _table_ = 'regions'
    id = orm.PrimaryKey(int)
    identifier = orm.Required(str)
    names = orm.Set("RegionName")
    generations = orm.Set(Generation)

class RegionName(db.Entity):
    _table_ = "region_names"
    region_id = orm.Required(Region)
    local_language_id = orm.Required(Language)
    name = orm.Required(str)
    orm.PrimaryKey(region_id, local_language_id)

class Type(db.Entity):
    """Any of the elemental types Pokémon and moves can have."""
    _table_ = 'types'
    id = orm.PrimaryKey(int)
    identifier = orm.Required(str)
    generation_id = orm.Required(Generation)
    # damage_class_id = orm.Optional('move_damage_classes.id')
    damage = orm.Optional("TypeEfficacy", reverse="damage_type_id")
    target = orm.Optional("TypeEfficacy", reverse="target_type_id")
    game_indices = orm.Set("TypeGameIndex")
    berry_natural_gift = orm.Set(Berry)
    names = orm.Set("TypeName")

class TypeName(db.Entity):
    _table_ = "type_names"
    type_id = orm.Required(Type)
    local_language_id = orm.Required(Language)
    name = orm.Required(str)
    orm.PrimaryKey(type_id, local_language_id)

class TypeEfficacy(db.Entity):
    """The damage multiplier used when a move of a particular type damages a
    Pokémon of a particular other type.
    """
    _table_ = 'type_efficacy'
    damage_type_id = orm.Required(Type)
    target_type_id = orm.Required(Type)
    damage_factor = orm.Required(int)
    orm.PrimaryKey(damage_type_id, target_type_id)

class TypeGameIndex(db.Entity):
    _table_ = 'type_game_indices'
    type_id = orm.Required(Type)
    generation_id = orm.Required(Generation)
    game_index = orm.Required(int)
    orm.PrimaryKey(type_id, generation_id)

class VersionGroup(db.Entity):
    """A group of versions, containing either two paired versions (such as Red
    and Blue) or a single game (such as Yellow).
    """
    _table_ = 'version_groups'
    id = orm.PrimaryKey(int)
    identifier = orm.Required(str)
    generation_id = orm.Required("Generation")
    order = orm.Optional(int)
    ability_flavor_text = orm.Set(AbilityFlavorText)
    item_flavor_text = orm.Set(ItemFlavorText)




class Characteristic(db.Entity):
    """Flavor text hinting at genes that appears in a Pokémon's summary."""
    _table_ = 'characteristics'
    id = orm.PrimaryKey(int)
    stat_id = orm.Required('stats.id')
    gene_mod_5 = orm.Required(int) index=True,

create_translation_table('characteristic_text', Characteristic, 'text',
    relation_lazy='joined',
    message = orm.Required(str) index=True,
)

class ConquestEpisode(db.Entity):
    """An episode from Pokémon Conquest: one of a bunch of mini-stories
    featuring a particular warrior.

    The main story, "The Legend of Ransei", also counts, even though it's not
    in the episode select menu and there's no way to replay it.
    """
    _table_ = 'conquest_episodes'
    id = Column(Integer, primary_key=True, autoincrement=True,
    identifier = orm.Required(str)

create_translation_table('conquest_episode_names', ConquestEpisode, 'names',
    relation_lazy='joined',
    name=orm.Required(str) index=True,
)

class ConquestEpisodeWarrior(db.Entity):
    """A warrior featured in an episode in Pokémon Conquest.

    This needs its own table because of the player having two episodes and
    there being two players.
    """
    _table_ = 'conquest_episode_warriors'
    episode_id = Column(Integer, ForeignKey('conquest_episodes.id'), primary_key=True,
    warrior_id = Column(Integer, ForeignKey('conquest_warriors.id'), primary_key=True,


class ConquestKingdom(db.Entity):
    """A kingdom in Pokémon Conquest."""
    _table_ = 'conquest_kingdoms'
    id = Column(Integer, primary_key=True, autoincrement=True,
    identifier = orm.Required(str)
    type_id = orm.Required('types.id')

create_translation_table('conquest_kingdom_names', ConquestKingdom, 'names',
    relation_lazy='joined',
    name=orm.Required(str) index=True,


)

class ConquestMaxLink(db.Entity):
    """The maximum link a warrior rank can reach with a Pokémon in Pokémon Conquest."""
    _table_ = 'conquest_max_links'
    warrior_rank_id = Column(Integer, ForeignKey('conquest_warrior_ranks.id'), primary_key=True,
    pokemon_species_id = Column(Integer, ForeignKey('pokemon_species.id'), primary_key=True,
    max_link = orm.Required(int)

class ConquestMoveData(db.Entity):
    """Data about a move in Pokémon Conquest."""
    _table_ = 'conquest_move_data'
    move_id = Column(Integer, ForeignKey('moves.id'), primary_key=True, autoincrement=False,
    power = orm.Optional(int)
    accuracy = orm.Optional(int)
    effect_chance = orm.Optional(int)
    effect_id = orm.Required('conquest_move_effects.id')
    range_id = orm.Required('conquest_move_ranges.id')
    displacement_id = orm.Optional('conquest_move_displacements.id')

    @property
    def star_rating(self):
        """Return the move's in-game power rating as a number of stars."""
        if not self.power:
            return 0
        else:
            stars = (self.power - 1) // 10
            stars = min(stars, 5)  # i.e. maximum of 5 stars
            stars = max(stars, 1)  # And minimum of 1
            return stars

class ConquestMoveDisplacement(db.Entity):
    """A way in which a move can cause the user or target to move to a
    different tile.

    If a move displaces its user, the move's range is relative to the user's
    original position.
    """
    _table_ = 'conquest_move_displacements'
    id = Column(Integer, primary_key=True, autoincrement=True,
    identifier = orm.Required(str)
    affects_target = orm.Required(bool)


create_translation_table('conquest_move_displacement_prose', ConquestMoveDisplacement, 'prose',
    name = Column(Unicode(79), nullable=True,
    short_effect = Column(UnicodeText, nullable=True,
    effect = Column(UnicodeText, nullable=True,
)

class ConquestMoveEffect(db.Entity):
    """An effect moves can have in Pokémon Conquest."""
    _table_ = 'conquest_move_effects'
    id = Column(Integer, primary_key=True, autoincrement=True,


create_translation_table('conquest_move_effect_prose', ConquestMoveEffect, 'prose',
    short_effect = Column(UnicodeText, nullable=True,
    effect = Column(UnicodeText, nullable=True,
)

class ConquestMoveRange(db.Entity):
    """A set of tiles moves can target in Pokémon Conquest."""
    _table_ = 'conquest_move_ranges'
    id = Column(Integer, primary_key=True, autoincrement=True,
    identifier = orm.Required(str)
    targets = orm.Required(int)

create_translation_table('conquest_move_range_prose', ConquestMoveRange, 'prose',
    name = Column(Unicode(79), nullable=True,
    description = Column(UnicodeText, nullable=True,
)

class ConquestPokemonAbility(db.Entity):
    """An ability a Pokémon species has in Pokémon Conquest."""
    _table_ = 'conquest_pokemon_abilities'
    pokemon_species_id = Column(Integer, ForeignKey('pokemon_species.id'), primary_key=True, nullable=False, autoincrement=False,
    slot = orm.PrimaryKey(int) autoincrement=False,
    ability_id = orm.Required('abilities.id')

class ConquestPokemonEvolution(db.Entity):
    """The conditions under which a Pokémon must successfully complete an
    action to evolve in Pokémon Conquest.

    Any condition may be null if it does not apply for a particular Pokémon.
    """
    _table_ = 'conquest_pokemon_evolution'
    evolved_species_id = Column(Integer, ForeignKey('pokemon_species.id'), primary_key=True, nullable=False,
    required_stat_id = orm.Optional('conquest_stats.id')
    minimum_stat = orm.Optional(int)
    minimum_link = orm.Optional(int)
    kingdom_id = orm.Optional('conquest_kingdoms.id')
    warrior_gender_id = orm.Optional('genders.id')
    item_id = orm.Optional('items.id')
    recruiting_ko_required = orm.Required(bool)

class ConquestPokemonMove(db.Entity):
    """A Pokémon's move in Pokémon Conquest.

    Yes, "move"; each Pokémon has exactly one.
    """
    _table_ = 'conquest_pokemon_moves'
    pokemon_species_id = Column(Integer, ForeignKey('pokemon_species.id'), primary_key=True, autoincrement=False,
    move_id = orm.Required('moves.id')

class ConquestPokemonStat(db.Entity):
    """A Pokémon's base stat in Pokémon Conquest.

    The main four base stats in Conquest are derived from level 100 stats in
    the main series (ignoring effort, genes, and natures).  Attack matches
    either Attack or Special Attack, and Defense matches the average of Defense
    and Special Defense.  HP and Speed are the same.
    """
    _table_ = 'conquest_pokemon_stats'
    pokemon_species_id = Column(Integer, ForeignKey('pokemon_species.id'), primary_key=True, autoincrement=False,
    conquest_stat_id = Column(Integer, ForeignKey('conquest_stats.id'), primary_key=True, autoincrement=False,
    base_stat = orm.Required(int)

class ConquestStat(db.Entity):
    """A stat Pokémon have in Pokémon Conquest."""
    _table_ = 'conquest_stats'
    id = Column(Integer, primary_key=True, autoincrement=True,
    identifier = orm.Required(str)
    is_base = orm.Required(bool)

create_translation_table('conquest_stat_names', ConquestStat, 'names',
    relation_lazy='joined',
    name=orm.Required(str) index=True,
)

class ConquestTransformationPokemon(db.Entity):
    """A Pokémon that satisfies a warrior transformation's link condition.

    If a warrior has one or more Pokémon listed here, they only need to raise
    one of them to the required link.
    """
    _table_ = 'conquest_transformation_pokemon'
    transformation_id = Column(Integer, ForeignKey('conquest_warrior_transformation.transformed_warrior_rank_id'), primary_key=True,
    pokemon_species_id = Column(Integer, ForeignKey('pokemon_species.id'), primary_key=True,

class ConquestTransformationWarrior(db.Entity):
    """A warrior who must be present in the same nation as another warrior for
    the latter to transform into their next rank.

    If a warrior has one or more other warriors listed here, they *all* need to
    gather in the same nation for the transformation to take place.
    """
    _table_ = 'conquest_transformation_warriors'
    transformation_id = Column(Integer, ForeignKey('conquest_warrior_transformation.transformed_warrior_rank_id'), primary_key=True,
    present_warrior_id = Column(Integer, ForeignKey('conquest_warriors.id'), primary_key=True,

class ConquestWarrior(db.Entity):
    """A warrior in Pokémon Conquest."""
    _table_ = 'conquest_warriors'
    id = orm.PrimaryKey(int) autoincrement=True,
    identifier = orm.Required(str)
    gender_id = orm.Required('genders.id')
    archetype_id = orm.Optional('conquest_warrior_archetypes.id')

create_translation_table('conquest_warrior_names', ConquestWarrior, 'names',
    relation_lazy='joined',
    name=orm.Required(str) index=True,
)

class ConquestWarriorArchetype(db.Entity):
    """An archetype that generic warriors in Pokémon Conquest can have.  All
    warriors of a particular archetype share sprites and dialogue.

    Some of these are unused as warriors because they exist only as NPCs.  They
    should still be kept because we have their sprites and may eventually get
    their dialogue.
    """
    _table_ = 'conquest_warrior_archetypes'
    id = Column(Integer, primary_key=True, autoincrement=True,
    identifier = orm.Required(str)

class ConquestWarriorRank(db.Entity):
    """A warrior at a particular rank in Pokémon Conquest.

    These are used for whatever changes between ranks, much like Pokémon forms.
    Generic warriors who have only one rank are also represented here, with a
    single row.

    To clarify, each warrior's ranks are individually called "warrior ranks"
    here; for example, "Rank 2 Nobunaga" is an example of a warrior rank, not
    just "Rank 2".
    """
    _table_ = 'conquest_warrior_ranks'
    id = Column(Integer, primary_key=True, autoincrement=True,

    warrior_id = orm.Required('conquest_warriors.id')

    rank = orm.Required(int)

    skill_id = orm.Required('conquest_warrior_skills.id')


    __table_args__ = (
        UniqueConstraint(warrior_id, rank),
        {},
    )

class ConquestWarriorRankStatMap(db.Entity):
    """Any of a warrior rank's warrior stats in Pokémon Conquest."""
    _table_ = 'conquest_warrior_rank_stat_map'
    warrior_rank_id = Column(Integer, ForeignKey('conquest_warrior_ranks.id'), primary_key=True, autoincrement=False,

    warrior_stat_id = Column(Integer, ForeignKey('conquest_warrior_stats.id'), primary_key=True, autoincrement=False,

    base_stat = orm.Required(int)


class ConquestWarriorSkill(db.Entity):
    """A warrior skill in Pokémon Conquest."""
    _table_ = 'conquest_warrior_skills'
    id = orm.PrimaryKey(int) autoincrement=True,

    identifier = orm.Required(str)



create_translation_table('conquest_warrior_skill_names', ConquestWarriorSkill, 'names',
    relation_lazy='joined',
    name=orm.Required(str) index=True,


)

class ConquestWarriorSpecialty(db.Entity):
    """A warrior's specialty types in Pokémon Conquest.

    These have no actual effect on gameplay; they just indicate which types of
    Pokémon each warrior generally has strong maximum links with.
    """
    _table_ = 'conquest_warrior_specialties'
    warrior_id = Column(Integer, ForeignKey('conquest_warriors.id'), primary_key=True, nullable=False, autoincrement=False,

    type_id = Column(Integer, ForeignKey('types.id'), primary_key=True, nullable=False, autoincrement=False,

    slot = orm.PrimaryKey(int) autoincrement=False,


class ConquestWarriorStat(db.Entity):
    """A stat that warriors have in Pokémon Conquest."""
    _table_ = 'conquest_warrior_stats'
    id = Column(Integer, primary_key=True, autoincrement=True,

    identifier = orm.Required(str)



create_translation_table('conquest_warrior_stat_names', ConquestWarriorStat, 'names',
    relation_lazy='joined',
    name=orm.Required(str) index=True,


)

class ConquestWarriorTransformation(db.Entity):
    """The conditions under which a warrior must perform an action in order
    to transform to the next rank.

    Or most of them, anyway.  See also ConquestTransformationPokemon and
    ConquestTransformationWarrior.
    """
    _table_ = 'conquest_warrior_transformation'
    transformed_warrior_rank_id = Column(Integer, ForeignKey('conquest_warrior_ranks.id'), primary_key=True,

    is_automatic = orm.Required(bool)

    required_link = orm.Optional(int)

    completed_episode_id = orm.Optional('conquest_episodes.id')

    current_episode_id = orm.Optional('conquest_episodes.id')

    distant_warrior_id = orm.Optional('conquest_warriors.id')

    female_warlord_count = orm.Optional(int)

    pokemon_count = orm.Optional(int)

    collection_type_id = orm.Optional('types.id')

    warrior_count = orm.Optional(int)


class ContestCombo(db.Entity):
    """Combo of two moves in a Contest."""
    _table_ = 'contest_combos'
    first_move_id = Column(Integer, ForeignKey('moves.id'), primary_key=True, nullable=False, autoincrement=False,

    second_move_id = Column(Integer, ForeignKey('moves.id'), primary_key=True, nullable=False, autoincrement=False,


class ContestEffect(db.Entity):
    """Effect of a move when used in a Contest."""
    _table_ = 'contest_effects'
    id = orm.PrimaryKey(int)

    appeal = Column(SmallInteger, nullable=False,

    jam = Column(SmallInteger, nullable=False,


create_translation_table('contest_effect_prose', ContestEffect, 'prose',
    flavor_text = Column(UnicodeText, nullable=True,


    effect = Column(UnicodeText, nullable=True,


)


class EggGroup(db.Entity):
    """An Egg group. Usually, two Pokémon can breed if they share an Egg Group.

    Exceptions:

    Pokémon in the No Eggs group cannot breed.

    Pokemon in the Ditto group can breed with any pokemon
    except those in the Ditto or No Eggs groups.

    ID matches to the internal ID used in the games.
    """
    _table_ = 'egg_groups'
    id = orm.PrimaryKey(int)
    identifier = orm.Required(str)



create_translation_table('egg_group_prose', EggGroup, 'names',
    relation_lazy='joined',
    name = orm.Required(str) index=True,


)

class Encounter(db.Entity):
    """Encounters with wild Pokémon.

    Bear with me, here.

    Within a given area in a given game, encounters are differentiated by the
    "slot" they are in and the state of the game world.

    What the player is doing to get an encounter, such as surfing or walking
    through tall grass, is called a method.  Each method has its own set of
    encounter slots.

    Within a method, slots are defined primarily by rarity.  Each slot can
    also be affected by world conditions; for example, the 20% slot for walking
    in tall grass is affected by whether a swarm is in effect in that area.
    "Is there a swarm?" is a condition; "there is a swarm" and "there is not a
    swarm" are the possible values of this condition.

    A slot (20% walking in grass) and any appropriate world conditions (no
    swarm) are thus enough to define a specific encounter.
    """

    _table_ = 'encounters'
    id = orm.PrimaryKey(int)

    version_id = orm.Required('versions.id') autoincrement=False,

    location_area_id = orm.Required('location_areas.id') autoincrement=False,

    encounter_slot_id = orm.Required('encounter_slots.id') autoincrement=False,

    pokemon_id = orm.Required('pokemon.id') autoincrement=False,

    min_level = orm.Required(int) autoincrement=False,

    max_level = orm.Required(int) autoincrement=False,


class EncounterCondition(db.Entity):
    """A condition in the game world that affects Pokémon encounters, such as time of day."""

    _table_ = 'encounter_conditions'
    id = orm.PrimaryKey(int)

    identifier = orm.Required(str)



create_translation_table('encounter_condition_prose', EncounterCondition, 'prose',
    name = orm.Required(str) index=True,


)

class EncounterConditionValue(db.Entity):
    """A possible state for a condition.

    For example, the state of 'swarm' could be 'swarm' or 'no swarm'.
    """

    _table_ = 'encounter_condition_values'
    id = orm.PrimaryKey(int)

    encounter_condition_id = Column(Integer, ForeignKey('encounter_conditions.id'), primary_key=False, nullable=False, autoincrement=False,

    identifier = orm.Required(str)


    is_default = orm.Required(bool)


create_translation_table('encounter_condition_value_prose', EncounterConditionValue, 'prose',
    name = orm.Required(str) index=True,


)

class EncounterConditionValueMap(db.Entity):
    """Maps encounters to the specific conditions under which they occur."""
    _table_ = 'encounter_condition_value_map'
    encounter_id = Column(Integer, ForeignKey('encounters.id'), primary_key=True, nullable=False, autoincrement=False,

    encounter_condition_value_id = Column(Integer, ForeignKey('encounter_condition_values.id'), primary_key=True, nullable=False, autoincrement=False,


class EncounterMethod(db.Entity):
    """A way the player can enter a wild encounter.

    For example, surfing, fishing, or walking through tall grass.
    """

    _table_ = 'encounter_methods'
    id = orm.PrimaryKey(int)

    identifier = orm.Required(str) unique=True,


    order = Column(Integer, unique=True, nullable=False,


create_translation_table('encounter_method_prose', EncounterMethod, 'prose',
    name = orm.Required(str) index=True,


)

class EncounterSlot(db.Entity):
    """An abstract "slot" within a method, associated with both some set of conditions and a rarity.

    "slot" has a very specific meaning:
    If during gameplay you know sufficient details about the current game state,
    you can predict which slot (and therefore which pokemon) will spawn.

    There are currently two reasons that "slot" might be empty:
    1) The slot corresponds to a gift pokemon.
    2) Red/Blue's Super Rod slots, which don't correspond to in-game slots.
       See https://github.com/veekun/pokedex/issues/166#issuecomment-220101455
    """

    _table_ = 'encounter_slots'
    id = orm.PrimaryKey(int)

    version_group_id = orm.Required('version_groups.id') autoincrement=False,

    encounter_method_id = Column(Integer, ForeignKey('encounter_methods.id'), primary_key=False, nullable=False, autoincrement=False,

    slot = orm.Optional(int)

    rarity = orm.Optional(int)


class EvolutionChain(db.Entity):
    """A family of Pokémon that are linked by evolution."""
    _table_ = 'evolution_chains'
    id = orm.PrimaryKey(int)

    baby_trigger_item_id = orm.Optional('items.id')


class EvolutionTrigger(db.Entity):
    """An evolution type, such as "level" or "trade". """
    _table_ = 'evolution_triggers'
    id = orm.PrimaryKey(int)

    identifier = orm.Required(str)



create_translation_table('evolution_trigger_prose', EvolutionTrigger, 'prose',
    name = orm.Required(str) index=True,


)

class Experience(db.Entity):
    """EXP needed for a certain level with a certain growth rate."""
    _table_ = 'experience'
    growth_rate_id = Column(Integer, ForeignKey('growth_rates.id'), primary_key=True, nullable=False,

    level = orm.PrimaryKey(int) autoincrement=False,

    experience = orm.Required(int)


class Gender(db.Entity):
    """A gender."""
    _table_ = 'genders'
    id = orm.PrimaryKey(int) autoincrement=True,

    identifier = orm.Required(str)




class GrowthRate(db.Entity):
    """Growth rate of a Pokémon, i.e. the EXP → level function. """
    _table_ = 'growth_rates'
    id = orm.PrimaryKey(int)

    identifier = orm.Required(str)


    formula = Column(UnicodeText, nullable=False,



create_translation_table('growth_rate_prose', GrowthRate, 'prose',
    name = orm.Required(str) index=True,


)


class Location(db.Entity):
    """A place in the Pokémon world."""
    _table_ = 'locations'
    id = orm.PrimaryKey(int)

    region_id = Column(Integer, ForeignKey('regions.id'),

    identifier = orm.Required(str) unique=True,



create_translation_table('location_names', Location, 'names',
    relation_lazy='joined',
    name = orm.Required(str) index=True,


    subtitle = Column(Unicode(79), nullable=True, index=False,

            This may be an alternate name for the locaton, as in the Kalos routes,
            or the name of a subarea of the location, as in Alola.""",

)

class LocationArea(db.Entity):
    """A sub-area of a location."""
    _table_ = 'location_areas'
    id = orm.PrimaryKey(int)

    location_id = orm.Required('locations.id')

    game_index = orm.Required(int)

    identifier = Column(Unicode(79), nullable=True,



    __table_args__ = (
        UniqueConstraint(location_id, identifier),
        {},
    )

create_translation_table('location_area_prose', LocationArea, 'prose',
    relation_lazy='joined',
    name = Column(Unicode(79), nullable=True, index=True,


)

class LocationAreaEncounterRate(db.Entity):
    """The chance of encountering a wild Pokémon in an area.

    In other words, how likely a step in tall grass is to trigger a wild battle.
    The exact meaning of the rate varies across versions but generally higher is
    more likely.
    """
    _table_ = 'location_area_encounter_rates'
    location_area_id = Column(Integer, ForeignKey('location_areas.id'), primary_key=True, nullable=False, autoincrement=False,

    encounter_method_id = Column(Integer, ForeignKey('encounter_methods.id'), primary_key=True, nullable=False, autoincrement=False,

    version_id = Column(Integer, ForeignKey('versions.id'), primary_key=True, autoincrement=False,

    rate = orm.Optional(int)


class LocationGameIndex(db.Entity):
    """IDs the games use internally for locations."""
    _table_ = 'location_game_indices'
    location_id = orm.Required('locations.id') primary_key=True,

    generation_id = orm.Required('generations.id') primary_key=True,

    game_index = orm.Required(int) primary_key=True, autoincrement=False,


class Machine(db.Entity):
    """A TM or HM; numbered item that can teach a move to a Pokémon."""
    _table_ = 'machines'
    machine_number = orm.PrimaryKey(int) autoincrement=False,

    version_group_id = Column(Integer, ForeignKey('version_groups.id'), primary_key=True, nullable=False, autoincrement=False,

    item_id = orm.Required('items.id')

    move_id = orm.Required('moves.id')


    @property
    def is_hm(self):
        """True if this machine is a HM, False if it's a TM."""
        return self.machine_number >= 100

class Move(db.Entity):
    """A Move: technique or attack a Pokémon can learn to use.

    IDs below 10000 match the internal IDs used in the games.
    IDs above 10000 are reserved for Shadow moves from Colosseum and XD."""
    _table_ = 'moves'
    id = orm.PrimaryKey(int)
    identifier = orm.Required(str)


    generation_id = orm.Required('generations.id')

    type_id = orm.Required('types.id')

    power = Column(SmallInteger, nullable=True,

    pp = Column(SmallInteger, nullable=True,

    accuracy = Column(SmallInteger, nullable=True,

    priority = Column(SmallInteger, nullable=False,

    target_id = orm.Required('move_targets.id')

    damage_class_id = orm.Required('move_damage_classes.id')

    effect_id = orm.Required('move_effects.id')

    effect_chance = orm.Optional(int)

    contest_type_id = orm.Optional('contest_types.id')

    contest_effect_id = orm.Optional('contest_effects.id')

    super_contest_effect_id = orm.Optional('super_contest_effects.id')


create_translation_table('move_names', Move, 'names',
    relation_lazy='joined',
    name = orm.Required(str) index=True,


)
create_translation_table('move_flavor_summaries', Move, 'flavor_summaries',
    flavor_summary = Column(UnicodeText, nullable=True,


)

class MoveBattleStyle(db.Entity):
    """Battle Palace style.

    See NatureBattleStylePreference.
    """
    _table_ = 'move_battle_styles'
    id = orm.PrimaryKey(int)

    identifier = orm.Required(str)



create_translation_table('move_battle_style_prose', MoveBattleStyle, 'prose',
    relation_lazy='joined',
    name = orm.Required(str) index=True,


)

class MoveChangelog(db.Entity):
    """History of changes to moves across main game versions."""
    _table_ = 'move_changelog'
    move_id = Column(Integer, ForeignKey('moves.id'), primary_key=True, nullable=False,

    changed_in_version_group_id = Column(Integer, ForeignKey('version_groups.id'), primary_key=True, nullable=False,

    type_id = orm.Optional('types.id')

    power = Column(SmallInteger, nullable=True,

    pp = Column(SmallInteger, nullable=True,

    accuracy = Column(SmallInteger, nullable=True,

    priority = Column(SmallInteger, nullable=True,

    target_id = orm.Optional('move_targets.id')

    effect_id = orm.Optional('move_effects.id')

    effect_chance = orm.Optional(int)


class MoveDamageClass(db.Entity):
    """Any of the damage classes moves can have, i.e. physical, special, or non-damaging."""
    _table_ = 'move_damage_classes'
    id = orm.PrimaryKey(int)

    identifier = orm.Required(str)



create_translation_table('move_damage_class_prose', MoveDamageClass, 'prose',
    relation_lazy='joined',
    name = Column(Unicode(79), nullable=True, index=True,


    description = Column(UnicodeText, nullable=True,


)

class MoveEffect(db.Entity):
    """An effect of a move."""
    _table_ = 'move_effects'
    id = orm.PrimaryKey(int)


create_translation_table('move_effect_prose', MoveEffect, 'prose',
    short_effect = Column(UnicodeText, nullable=True,


    effect = Column(UnicodeText, nullable=True,


)

class MoveEffectChangelog(db.Entity):
    """History of changes to move effects across main game versions."""
    _table_ = 'move_effect_changelog'
    id = orm.PrimaryKey(int)

    effect_id = orm.Required('move_effects.id')

    changed_in_version_group_id = orm.Required('version_groups.id')


    __table_args__ = (
        UniqueConstraint(effect_id, changed_in_version_group_id),
        {},
    )

create_translation_table('move_effect_changelog_prose', MoveEffectChangelog, 'prose',
    effect = Column(UnicodeText, nullable=False,


)

class MoveFlag(db.Entity):
    """A Move attribute such as "snatchable" or "contact". """
    _table_ = 'move_flags'
    id = orm.PrimaryKey(int)

    identifier = orm.Required(str)



class MoveFlagMap(db.Entity):
    """Maps a move flag to a move."""
    _table_ = 'move_flag_map'
    move_id = Column(Integer, ForeignKey('moves.id'), primary_key=True, nullable=False, autoincrement=False,

    move_flag_id = Column(Integer, ForeignKey('move_flags.id'), primary_key=True, nullable=False, autoincrement=False,


create_translation_table('move_flag_prose', MoveFlag, 'prose',
    relation_lazy='joined',
    name = Column(Unicode(79), nullable=True, index=True,


    description = Column(UnicodeText, nullable=True,


)

class MoveFlavorText(db.Entity):
    """In-game description of a move."""
    _table_ = 'move_flavor_text'
    summary_column = Move.flavor_summaries_table, 'flavor_summary'
    move_id = Column(Integer, ForeignKey('moves.id'), primary_key=True, nullable=False, autoincrement=False,

    version_group_id = Column(Integer, ForeignKey('version_groups.id'), primary_key=True, nullable=False, autoincrement=False,

    language_id = Column(Integer, ForeignKey('languages.id'), primary_key=True, nullable=False,

    flavor_text = Column(UnicodeText, nullable=False,



class MoveMeta(db.Entity):
    """Metadata for move effects, sorta-kinda ripped straight from the game."""
    _table_ = 'move_meta'
    move_id = Column(Integer, ForeignKey('moves.id'), primary_key=True, nullable=False, autoincrement=False,

    meta_category_id = orm.Required('move_meta_categories.id')

    meta_ailment_id = orm.Required('move_meta_ailments.id')

    min_hits = orm.Optional(int) index=True,

    max_hits = orm.Optional(int) index=True,

    min_turns = orm.Optional(int) index=True,

    max_turns = orm.Optional(int) index=True,

    drain = orm.Required(int) index=True,

    healing = orm.Required(int) index=True,

    crit_rate = orm.Required(int) index=True,

    ailment_chance = orm.Required(int) index=True,

    flinch_chance = orm.Required(int) index=True,

    stat_chance = orm.Required(int) index=True,


    @hybrid_property
    def recoil(self):
        """Recoil damage or HP drain; the opposite of `drain`. """
        return -self.drain

class MoveMetaAilment(db.Entity):
    """Common status ailments moves can inflict on a single Pokémon, including
    major ailments like paralysis and minor ailments like trapping.
    """
    _table_ = 'move_meta_ailments'
    id = orm.PrimaryKey(int) autoincrement=False,

    identifier = orm.Required(str) index=True, unique=True,



create_translation_table('move_meta_ailment_names', MoveMetaAilment, 'names',
    relation_lazy='joined',
    name = orm.Required(str) index=True,


)

class MoveMetaCategory(db.Entity):
    """Very general categories that loosely group move effects."""
    _table_ = 'move_meta_categories'
    id = orm.PrimaryKey(int) autoincrement=False,

    identifier = orm.Required(str) index=True, unique=True,



create_translation_table('move_meta_category_prose', MoveMetaCategory, 'prose',
    relation_lazy='joined',
    description = Column(UnicodeText, nullable=False,


)

class MoveMetaStatChange(db.Entity):
    """Stat changes moves (may) make."""
    _table_ = 'move_meta_stat_changes'
    move_id = Column(Integer, ForeignKey('moves.id'), primary_key=True, nullable=False, autoincrement=False,

    stat_id = Column(Integer, ForeignKey('stats.id'), primary_key=True, nullable=False, autoincrement=False,

    change = orm.Required(int) index=True,


class MoveTarget(db.Entity):
    """Targeting or "range" of a move, e.g. "Affects all opponents" or "Affects user". """
    _table_ = 'move_targets'
    id = orm.PrimaryKey(int)

    identifier = orm.Required(str)



create_translation_table('move_target_prose', MoveTarget, 'prose',
    relation_lazy='joined',
    name = Column(Unicode(79), nullable=True, index=True,


    description = Column(UnicodeText, nullable=True,


)

class Nature(db.Entity):
    """A nature a Pokémon can have, such as Calm or Brave."""
    _table_ = 'natures'
    id = orm.PrimaryKey(int)

    identifier = orm.Required(str)


    decreased_stat_id = orm.Required('stats.id')

    increased_stat_id = orm.Required('stats.id')

    hates_flavor_id = orm.Required('contest_types.id')

    likes_flavor_id = orm.Required('contest_types.id')

    game_index = Column(Integer, unique=True, nullable=False,


    @property
    def is_neutral(self):
        """Returns True iff this nature doesn't alter a Pokémon's stats,
        bestow taste preferences, etc.
        """
        return self.increased_stat_id == self.decreased_stat_id

create_translation_table('nature_names', Nature, 'names',
    relation_lazy='joined',
    name = orm.Required(str) index=True,


)

class NatureBattleStylePreference(db.Entity):
    """Battle Palace move preference.

    Specifies how likely a Pokémon with a specific Nature is to use a move of
    a particular battle style in Battle Palace or Battle Tent.
    """
    _table_ = 'nature_battle_style_preferences'
    nature_id = Column(Integer, ForeignKey('natures.id'), primary_key=True, nullable=False,

    move_battle_style_id = Column(Integer, ForeignKey('move_battle_styles.id'), primary_key=True, nullable=False,

    low_hp_preference = orm.Required(int)

    high_hp_preference = orm.Required(int)


class NaturePokeathlonStat(db.Entity):
    """Specifies how a Nature affects a Pokéathlon stat."""
    _table_ = 'nature_pokeathlon_stats'
    nature_id = Column(Integer, ForeignKey('natures.id'), primary_key=True, nullable=False,

    pokeathlon_stat_id = Column(Integer, ForeignKey('pokeathlon_stats.id'), primary_key=True, nullable=False,

    max_change = orm.Required(int)


class PalPark(db.Entity):
    """Data for the Pal Park mini-game in Generation IV."""

    _table_ = 'pal_park'

    species_id = Column(Integer, ForeignKey('pokemon_species.id'), primary_key=True,


    area_id = orm.Required('pal_park_areas.id')

    base_score = orm.Required(int)

    rate = orm.Required(int)


class PalParkArea(db.Entity):
    """A distinct area of Pal Park in which Pokémon appear."""
    _table_ = 'pal_park_areas'

    id = orm.PrimaryKey(int)

    identifier = orm.Required(str)



create_translation_table('pal_park_area_names', PalParkArea, 'names',
    name = orm.Required(str) index=True,


)

class PokeathlonStat(db.Entity):
    """A Pokéathlon stat, such as "Stamina" or "Jump". """
    _table_ = 'pokeathlon_stats'
    id = orm.PrimaryKey(int)

    identifier = orm.Required(str)



create_translation_table('pokeathlon_stat_names', PokeathlonStat, 'names',
    name = orm.Required(str) index=True,


)

class Pokedex(db.Entity):
    """A collection of Pokémon species ordered in a particular way."""
    _table_ = 'pokedexes'
    id = orm.PrimaryKey(int)

    region_id = orm.Optional('regions.id')

    identifier = orm.Required(str)


    is_main_series = orm.Required(bool)


create_translation_table('pokedex_prose', Pokedex, 'prose',
    relation_lazy='joined',
    name = Column(Unicode(79), nullable=True, index=True,


    description = Column(UnicodeText, nullable=True,


)

class PokedexVersionGroup(db.Entity):
    """A mapping from Pokédexes to version groups in which they appear as the regional dex."""
    _table_ = 'pokedex_version_groups'
    pokedex_id = Column(Integer, ForeignKey('pokedexes.id'), primary_key=True,

    version_group_id = Column(Integer, ForeignKey('version_groups.id'), primary_key=True,




class PokemonColor(db.Entity):
    """The "Pokédex color" of a Pokémon species. Usually based on the Pokémon's color. """
    _table_ = 'pokemon_colors'
    id = orm.PrimaryKey(int) autoincrement=False,

    identifier = orm.Required(str)



create_translation_table('pokemon_color_names', PokemonColor, 'names',
    relation_lazy='joined',
    name = orm.Required(str) index=True,


)

class PokemonDexNumber(db.Entity):
    """The number of a species in a particular Pokédex (e.g. Jigglypuff is #138 in Hoenn's 'dex)."""
    _table_ = 'pokemon_dex_numbers'
    species_id = Column(Integer, ForeignKey('pokemon_species.id'), primary_key=True, nullable=False, autoincrement=False,

    pokedex_id = Column(Integer, ForeignKey('pokedexes.id'), primary_key=True, nullable=False, autoincrement=False,

    pokedex_number = orm.Required(int)


    __table_args__ = (
        UniqueConstraint(pokedex_id, pokedex_number),
        UniqueConstraint(pokedex_id, species_id),
        {},
    )


class PokemonEggGroup(db.Entity):
    """Maps an Egg group to a species; each species belongs to one or two egg groups."""
    _table_ = 'pokemon_egg_groups'
    species_id = Column(Integer, ForeignKey('pokemon_species.id'), primary_key=True, nullable=False, autoincrement=False,

    egg_group_id = Column(Integer, ForeignKey('egg_groups.id'), primary_key=True, nullable=False, autoincrement=False,


class PokemonEvolution(db.Entity):
    """A required action ("trigger") and the conditions under which the trigger
    must occur to cause a Pokémon to evolve.

    Any condition may be null if it does not apply for a particular Pokémon.
    """
    _table_ = 'pokemon_evolution'
    id = orm.PrimaryKey(int)

    evolved_species_id = orm.Required('pokemon_species.id')

    evolution_trigger_id = orm.Required('evolution_triggers.id')

    trigger_item_id = orm.Optional('items.id')

    minimum_level = orm.Optional(int)

    gender_id = orm.Optional('genders.id')

    location_id = orm.Optional('locations.id')

    held_item_id = orm.Optional('items.id')

    time_of_day = Column(Enum('day', 'night', 'dusk', name='pokemon_evolution_time_of_day'), nullable=True,

    known_move_id = orm.Optional('moves.id')

    known_move_type_id = orm.Optional('types.id')

    minimum_happiness = orm.Optional(int)

    minimum_beauty = orm.Optional(int)

    minimum_affection = orm.Optional(int)

    relative_physical_stats = orm.Optional(int)

    party_species_id = orm.Optional('pokemon_species.id')

    party_type_id = orm.Optional('types.id')

    trade_species_id = orm.Optional('pokemon_species.id')

    needs_overworld_rain = orm.Required(bool)

    turn_upside_down = orm.Required(bool)


class PokemonForm(db.Entity):
    """An individual form of a Pokémon.  This includes *every* variant (except
    color differences) of every Pokémon, regardless of how the games treat
    them.  Even Pokémon with no alternate forms have one row in this table, to
    represent their lone "normal" form.

    Forms which are not the default for their species have IDs above 10000.
    IDs below 10000 correspond to ID of the species for convenience,
    but this should not be relied upon.
    To get the species ID of a form, join with the pokemon table.
    """
    _table_ = 'pokemon_forms'
    id = orm.PrimaryKey(int)
    identifier = orm.Required(str)


    form_identifier = Column(Unicode(79), nullable=True,


    pokemon_id = orm.Required('pokemon.id') autoincrement=False,

    introduced_in_version_group_id = Column(Integer, ForeignKey('version_groups.id'), autoincrement=False,

    is_default = orm.Required(bool)

    is_battle_only = orm.Required(bool)

    is_mega = orm.Required(bool)

    form_order = orm.Required(int) autoincrement=False,


            Multiple forms may have equal order, in which case they should fall
            back on sorting by name.  Used in generating `pokemon_forms.order`
            and `pokemon.order`.
            """)
    order = orm.Required(int) autoincrement=False,


    @property
    def name(self):
        """Name of this form: the form_name, if set; otherwise the species name."""
        return self.pokemon_name or self.species.name

create_translation_table('pokemon_form_names', PokemonForm, 'names',
    relation_lazy='joined',
    form_name = Column(Unicode(79), nullable=True, index=True,


    pokemon_name = Column(Unicode(79), nullable=True, index=True,


)

class PokemonFormGeneration(db.Entity):
    """Links Pokémon forms to the generations they exist in."""
    _table_ = 'pokemon_form_generations'
    pokemon_form_id = Column(Integer, ForeignKey('pokemon_forms.id'), primary_key=True, nullable=False, autoincrement=False,

    generation_id = Column(Integer, ForeignKey('generations.id'), primary_key=True, nullable=False, autoincrement=False,

    game_index = orm.Required(int)


class PokemonFormPokeathlonStat(db.Entity):
    """A Pokémon form's performance in one Pokéathlon stat."""
    _table_ = 'pokemon_form_pokeathlon_stats'
    pokemon_form_id = Column(Integer, ForeignKey('pokemon_forms.id'), primary_key=True, nullable=False, autoincrement=False,

    pokeathlon_stat_id = Column(Integer, ForeignKey('pokeathlon_stats.id'), primary_key=True, nullable=False, autoincrement=False,

    minimum_stat = orm.Required(int) autoincrement=False,

    base_stat = orm.Required(int) autoincrement=False,

    maximum_stat = orm.Required(int) autoincrement=False,


class PokemonGameIndex(db.Entity):
    """The number of a Pokémon a game uses internally."""
    _table_ = 'pokemon_game_indices'
    pokemon_id = Column(Integer, ForeignKey('pokemon.id'), primary_key=True, autoincrement=False, nullable=False,

    version_id = Column(Integer, ForeignKey('versions.id'), primary_key=True, autoincrement=False, nullable=False,

    game_index = orm.Required(int)


class PokemonHabitat(db.Entity):
    """The habitat of a Pokémon, as given in the FireRed/LeafGreen version Pokédex."""
    _table_ = 'pokemon_habitats'
    id = orm.PrimaryKey(int) autoincrement=False,

    identifier = orm.Required(str)



create_translation_table('pokemon_habitat_names', PokemonHabitat, 'names',
    relation_lazy='joined',
    name = orm.Required(str) index=True,


)

class PokemonItem(db.Entity):
    """Record of an item a Pokémon can hold in the wild."""
    _table_ = 'pokemon_items'
    pokemon_id = Column(Integer, ForeignKey('pokemon.id'), primary_key=True, nullable=False, autoincrement=False,

    version_id = Column(Integer, ForeignKey('versions.id'), primary_key=True, nullable=False, autoincrement=False,

    item_id = Column(Integer, ForeignKey('items.id'), primary_key=True, nullable=False, autoincrement=False,

    rarity = orm.Required(int)


class PokemonMove(db.Entity):
    """Record of a move a Pokémon can learn."""
    _table_ = 'pokemon_moves'
    pokemon_id = orm.Required('pokemon.id') index=True,

    version_group_id = orm.Required('version_groups.id') index=True,

    move_id = orm.Required('moves.id') index=True,

    pokemon_move_method_id = orm.Required('pokemon_move_methods.id') index=True,

    level = orm.Optional(int) index=True, autoincrement=False,

    order = orm.Optional(int)


    __table_args__ = (
        PrimaryKeyConstraint('pokemon_id', 'version_group_id', 'move_id', 'pokemon_move_method_id', 'level'),
        {},
    )

class PokemonMoveMethod(db.Entity):
    """A method a move can be learned by, such as "Level up" or "Tutor". """
    _table_ = 'pokemon_move_methods'
    id = orm.PrimaryKey(int) autoincrement=False,

    identifier = orm.Required(str)



create_translation_table('pokemon_move_method_prose', PokemonMoveMethod, 'prose',
    relation_lazy='joined',
    name = Column(Unicode(79), nullable=True, index=True,


    description = Column(UnicodeText, nullable=True,


)

class PokemonShape(db.Entity):
    """The shape of a Pokémon's body.  Used for flavor in generation IV and V Pokédexes. """
    _table_ = 'pokemon_shapes'
    id = orm.PrimaryKey(int)

    identifier = orm.Required(str)



create_translation_table('pokemon_shape_prose', PokemonShape, 'prose',
    relation_lazy='joined',
    name = Column(Unicode(79), nullable=True, index=True,


    awesome_name = Column(Unicode(79), nullable=True,


    description = Column(UnicodeText, nullable=True,


)

class PokemonSpecies(db.Entity):
    """A Pokémon species: the standard 1–151.  Or 649.  Whatever.

    ID matches the National Pokédex number of the species.
    """
    _table_ = 'pokemon_species'
    id = orm.PrimaryKey(int)
    identifier = orm.Required(str)


    generation_id = Column(Integer, ForeignKey('generations.id'),

    evolves_from_species_id = orm.Optional('pokemon_species.id')

    evolution_chain_id = Column(Integer, ForeignKey('evolution_chains.id'),

    color_id = orm.Required('pokemon_colors.id')

    shape_id = orm.Optional('pokemon_shapes.id')

    habitat_id = orm.Optional('pokemon_habitats.id')

    gender_rate = orm.Required(int)

    capture_rate = orm.Required(int)

    base_happiness = orm.Required(int)

    is_baby = orm.Required(bool)

    hatch_counter = orm.Required(int)

    has_gender_differences = orm.Required(bool)

    growth_rate_id = orm.Required('growth_rates.id')

    forms_switchable = orm.Required(bool)

    is_legendary = orm.Required(bool)

    is_mythical = orm.Required(bool)

    order = orm.Required(int) index=True,

    conquest_order = orm.Optional(int) index=True,


create_translation_table('pokemon_species_names', PokemonSpecies, 'names',
    relation_lazy='joined',
    name = Column(Unicode(79), nullable=True, index=True,


    genus = Column(UnicodeText, nullable=True,


)
create_translation_table('pokemon_species_flavor_summaries', PokemonSpecies, 'flavor_summaries',
    flavor_summary = Column(UnicodeText, nullable=True,


)
create_translation_table('pokemon_species_prose', PokemonSpecies, 'prose',
    form_description = Column(UnicodeText, nullable=True,


)

class PokemonSpeciesFlavorText(db.Entity):
    """In-game Pokédex description of a Pokémon."""
    _table_ = 'pokemon_species_flavor_text'
    summary_column = PokemonSpecies.flavor_summaries_table, 'flavor_summary'
    species_id = Column(Integer, ForeignKey('pokemon_species.id'), primary_key=True, nullable=False, autoincrement=False,

    version_id = Column(Integer, ForeignKey('versions.id'), primary_key=True, nullable=False, autoincrement=False,

    language_id = Column(Integer, ForeignKey('languages.id'), primary_key=True, nullable=False,

    flavor_text = Column(UnicodeText, nullable=False,



class PokemonStat(db.Entity):
    """A stat value of a Pokémon."""
    _table_ = 'pokemon_stats'
    pokemon_id = Column(Integer, ForeignKey('pokemon.id'), primary_key=True, nullable=False, autoincrement=False,

    stat_id = Column(Integer, ForeignKey('stats.id'), primary_key=True, nullable=False, autoincrement=False,

    base_stat = orm.Required(int)

    effort = orm.Required(int)


class PokemonType(db.Entity):
    """Maps a type to a Pokémon. Each Pokémon has 1 or 2 types."""
    _table_ = 'pokemon_types'
    pokemon_id = Column(Integer, ForeignKey('pokemon.id'), primary_key=True, nullable=False, autoincrement=False,

    type_id = orm.Required('types.id')

    slot = orm.PrimaryKey(int) autoincrement=False,


class Stat(db.Entity):
    """A Stat, such as Attack or Speed."""
    _table_ = 'stats'
    id = orm.PrimaryKey(int)

    damage_class_id = orm.Optional('move_damage_classes.id')

    identifier = orm.Required(str)


    is_battle_only = orm.Required(bool)

    game_index = orm.Optional(int)


create_translation_table('stat_names', Stat, 'names',
    relation_lazy='joined',
    name = orm.Required(str) index=True,


)

class SuperContestCombo(db.Entity):
    """Combo of two moves in a Super Contest."""
    _table_ = 'super_contest_combos'
    first_move_id = Column(Integer, ForeignKey('moves.id'), primary_key=True, nullable=False, autoincrement=False,

    second_move_id = Column(Integer, ForeignKey('moves.id'), primary_key=True, nullable=False, autoincrement=False,


class SuperContestEffect(db.Entity):
    """An effect a move can have when used in the Super Contest."""
    _table_ = 'super_contest_effects'
    id = orm.PrimaryKey(int)

    appeal = Column(SmallInteger, nullable=False,


create_translation_table('super_contest_effect_prose', SuperContestEffect, 'prose',
    flavor_text = Column(UnicodeText, nullable=False,


)

class Version(db.Entity):
    _table_ = 'versions'
    id = orm.PrimaryKey(int)
    version_group_id = orm.Required('version_groups.id')

    identifier = orm.Required(str)



create_translation_table('version_names', Version, 'names',
    relation_lazy='joined',
    name = orm.Required(str) index=True,


)



class VersionGroupPokemonMoveMethod(db.Entity):
    """Maps a version group to a move learn methods it supports.

    "Supporting" means simply that the method appears in the game.
    For example, Breeding didn't exist in Gen.I, so it's not in this table.
    """
    _table_ = 'version_group_pokemon_move_methods'
    version_group_id = Column(Integer, ForeignKey('version_groups.id'), primary_key=True, nullable=False,

    pokemon_move_method_id = Column(Integer, ForeignKey('pokemon_move_methods.id'), primary_key=True, nullable=False,


class VersionGroupRegion(db.Entity):
    """Maps a version group to a region that appears in it."""
    _table_ = 'version_group_regions'
    version_group_id = Column(Integer, ForeignKey('version_groups.id'), primary_key=True, nullable=False,

    region_id = Column(Integer, ForeignKey('regions.id'), primary_key=True, nullable=False,



### Relationships down here, to avoid dependency ordering problems

Ability.changelog = relationship(AbilityChangelog,
    order_by=AbilityChangelog.changed_in_version_group_id.desc(),
    backref=backref('ability', innerjoin=True, lazy='joined'))
Ability.flavor_text = relationship(AbilityFlavorText,
    order_by=AbilityFlavorText.version_group_id,
    backref=backref('ability', innerjoin=True, lazy='joined'))
Ability.generation = relationship(Generation,
    innerjoin=True,
    backref='abilities')

AbilityChangelog.changed_in = relationship(VersionGroup,
    innerjoin=True, lazy='joined',
    backref='ability_changelog')

AbilityFlavorText.version_group = relationship(VersionGroup,
    innerjoin=True)
AbilityFlavorText.language = relationship(Language,
    innerjoin=True, lazy='joined')


Berry.berry_firmness = relationship(BerryFirmness,
    innerjoin=True,
    backref='berries')
Berry.firmness = association_proxy('berry_firmness', 'name')
Berry.flavors = relationship(BerryFlavor,
    order_by=BerryFlavor.contest_type_id,
    backref=backref('berry', innerjoin=True))
Berry.natural_gift_type = relationship(Type, innerjoin=True)

BerryFlavor.contest_type = relationship(ContestType, innerjoin=True)


Characteristic.stat = relationship(Stat,
    innerjoin=True,
    backref='characteristics')


ConquestEpisode.warriors = relationship(ConquestWarrior,
    secondary=ConquestEpisodeWarrior.__table__,
    innerjoin=True,
    backref='episodes')

ConquestKingdom.type = relationship(Type,
    uselist=False,
    innerjoin=True, lazy='joined',
    backref=backref('conquest_kingdom', uselist=False))

ConquestMaxLink.pokemon = relationship(PokemonSpecies,
    uselist=False,
    innerjoin=True, lazy='joined',
    backref=backref('conquest_max_links', lazy='dynamic',
                    order_by=ConquestMaxLink.warrior_rank_id))
ConquestMaxLink.warrior_rank = relationship(ConquestWarriorRank,
    uselist=False,
    innerjoin=True, lazy='joined',
    backref=backref('max_links', lazy='dynamic'))
ConquestMaxLink.warrior = association_proxy('warrior_rank', 'warrior')

ConquestMoveData.move_displacement = relationship(ConquestMoveDisplacement,
    uselist=False,
    backref='move_data')
ConquestMoveData.move = relationship(Move,
    uselist=False,
    innerjoin=True, lazy='joined',
    backref=backref('conquest_data', uselist=False))
ConquestMoveData.move_effect = relationship(ConquestMoveEffect,
    innerjoin=True, lazy='joined',
    backref='move_data')
ConquestMoveData.range = relationship(ConquestMoveRange,
    innerjoin=True, lazy='joined',
    backref='move_data')

ConquestMoveData.effect = markdown.MoveEffectProperty('effect')
ConquestMoveData.effect_map = markdown.MoveEffectPropertyMap('effect_map')
ConquestMoveData.short_effect = markdown.MoveEffectProperty('short_effect')
ConquestMoveData.short_effect_map = markdown.MoveEffectPropertyMap('short_effect_map')
ConquestMoveData.displacement = markdown.MoveEffectProperty('effect', relationship='move_displacement')

ConquestPokemonEvolution.gender = relationship(Gender,
    backref='conquest_evolutions')
ConquestPokemonEvolution.item = relationship(Item,
    backref='conquest_evolutions')
ConquestPokemonEvolution.kingdom = relationship(ConquestKingdom,
    backref='evolutions')
ConquestPokemonEvolution.stat = relationship(ConquestStat,
    backref='evolutions')

ConquestPokemonStat.pokemon = relationship(PokemonSpecies,
    uselist=False,
    innerjoin=True, lazy='joined',
    backref='conquest_stats')
ConquestPokemonStat.stat = relationship(ConquestStat,
    uselist=False,
    innerjoin=True, lazy='joined',
    backref='pokemon_stats')

ConquestWarrior.archetype = relationship(ConquestWarriorArchetype,
    uselist=False,
    backref=backref('warriors'))
ConquestWarrior.ranks = relationship(ConquestWarriorRank,
    order_by=ConquestWarriorRank.rank,
    innerjoin=True,
    backref=backref('warrior', uselist=False))
ConquestWarrior.types = relationship(Type,
    secondary=ConquestWarriorSpecialty.__table__,
    order_by=ConquestWarriorSpecialty.slot,
    innerjoin=True,
    backref='conquest_warriors')

ConquestWarriorRank.skill = relationship(ConquestWarriorSkill,
    uselist=False,
    innerjoin=True, lazy='joined',
    backref=backref('warrior_ranks', order_by=ConquestWarriorRank.id))
ConquestWarriorRank.stats = relationship(ConquestWarriorRankStatMap,
    innerjoin=True,
    order_by=ConquestWarriorRankStatMap.warrior_stat_id,
    backref=backref('warrior_rank', uselist=False, innerjoin=True, lazy='joined'))

ConquestWarriorRankStatMap.stat = relationship(ConquestWarriorStat,
    innerjoin=True, lazy='joined',
    uselist=False,
    backref='stat_map')

ConquestWarriorTransformation.completed_episode = relationship(ConquestEpisode,
    primaryjoin=ConquestWarriorTransformation.completed_episode_id==ConquestEpisode.id,
    uselist=False)
ConquestWarriorTransformation.current_episode = relationship(ConquestEpisode,
    primaryjoin=ConquestWarriorTransformation.current_episode_id==ConquestEpisode.id,
    uselist=False)
ConquestWarriorTransformation.distant_warrior = relationship(ConquestWarrior,
    uselist=False)
ConquestWarriorTransformation.pokemon = relationship(PokemonSpecies,
    secondary=ConquestTransformationPokemon.__table__,
    order_by=PokemonSpecies.conquest_order)
ConquestWarriorTransformation.present_warriors = relationship(ConquestWarrior,
    secondary=ConquestTransformationWarrior.__table__,
    order_by=ConquestWarrior.id)
ConquestWarriorTransformation.type = relationship(Type,
    uselist=False)
ConquestWarriorTransformation.warrior_rank = relationship(ConquestWarriorRank,
    uselist=False,
    innerjoin=True, lazy='joined',
    backref=backref('transformation', uselist=False, innerjoin=True))


ContestCombo.first = relationship(Move,
    primaryjoin=ContestCombo.first_move_id==Move.id,
    innerjoin=True, lazy='joined',
    backref='contest_combo_first')
ContestCombo.second = relationship(Move,
    primaryjoin=ContestCombo.second_move_id==Move.id,
    innerjoin=True, lazy='joined',
    backref='contest_combo_second')


Encounter.condition_values = relationship(EncounterConditionValue,
    secondary=EncounterConditionValueMap.__table__)
Encounter.location_area = relationship(LocationArea,
    innerjoin=True, lazy='joined',
    backref='encounters')
Encounter.pokemon = relationship(Pokemon,
    innerjoin=True, lazy='joined',
    backref='encounters')
Encounter.version = relationship(Version,
    innerjoin=True, lazy='joined',
    backref='encounters')
Encounter.slot = relationship(EncounterSlot,
    innerjoin=True, lazy='joined',
    backref='encounters')

EncounterConditionValue.condition = relationship(EncounterCondition,
    innerjoin=True, lazy='joined',
    backref='values')

EncounterSlot.method = relationship(EncounterMethod,
    innerjoin=True, lazy='joined',
    backref='slots')
EncounterSlot.version_group = relationship(VersionGroup, innerjoin=True)


EvolutionChain.baby_trigger_item = relationship(Item,
    backref='evolution_chains')


Experience.growth_rate = relationship(GrowthRate,
    innerjoin=True, lazy='joined',
    backref='experience_table')


Generation.versions = relationship(Version,
    secondary=VersionGroup.__table__,
    innerjoin=True)
Generation.main_region = relationship(Region, innerjoin=True)


GrowthRate.max_experience_obj = relationship(Experience,
    primaryjoin=and_(
        Experience.growth_rate_id == GrowthRate.id,
        Experience.level == 100),
    uselist=False, innerjoin=True)
GrowthRate.max_experience = association_proxy('max_experience_obj', 'experience')


Item.berry = relationship(Berry,
    uselist=False,
    backref='item')
Item.flags = relationship(ItemFlag,
    secondary=ItemFlagMap.__table__)
Item.flavor_text = relationship(ItemFlavorText,
    order_by=ItemFlavorText.version_group_id.asc(),
    backref=backref('item', innerjoin=True, lazy='joined'))
Item.fling_effect = relationship(ItemFlingEffect,
    backref='items')
Item.machines = relationship(Machine,
    order_by=Machine.version_group_id.asc())
Item.category = relationship(ItemCategory,
    innerjoin=True,
    backref=backref('items', order_by=Item.identifier.asc()))
Item.pocket = association_proxy('category', 'pocket')

ItemCategory.pocket = relationship(ItemPocket, innerjoin=True)

ItemFlavorText.version_group = relationship(VersionGroup,
    innerjoin=True, lazy='joined')
ItemFlavorText.language = relationship(Language,
    innerjoin=True, lazy='joined')

ItemGameIndex.item = relationship(Item,
    innerjoin=True, lazy='joined',
    backref='game_indices')
ItemGameIndex.generation = relationship(Generation,
    innerjoin=True, lazy='joined')

ItemPocket.categories = relationship(ItemCategory,
    innerjoin=True,
    order_by=ItemCategory.identifier.asc())


Location.region = relationship(Region,
    innerjoin=True,
    backref='locations')

LocationArea.location = relationship(Location,
    innerjoin=True, lazy='joined',
    backref='areas')

LocationAreaEncounterRate.location_area = relationship(LocationArea,
    innerjoin=True,
    backref='encounter_rates')
LocationAreaEncounterRate.method = relationship(EncounterMethod,
    innerjoin=True)

LocationGameIndex.location = relationship(Location,
    innerjoin=True, lazy='joined',
    backref='game_indices')
LocationGameIndex.generation = relationship(Generation,
    innerjoin=True, lazy='joined')


Machine.item = relationship(Item)
Machine.version_group = relationship(VersionGroup,
    innerjoin=True, lazy='joined')


Move.changelog = relationship(MoveChangelog,
    order_by=MoveChangelog.changed_in_version_group_id.desc(),
    backref=backref('move', innerjoin=True, lazy='joined'))
Move.contest_effect = relationship(ContestEffect,
    backref='moves')
Move.contest_combo_next = association_proxy('contest_combo_first', 'second')
Move.contest_combo_prev = association_proxy('contest_combo_second', 'first')
Move.contest_type = relationship(ContestType,
    backref='moves')
Move.damage_class = relationship(MoveDamageClass,
    innerjoin=True,
    backref='moves')
Move.flags = association_proxy('move_flags', 'flag')
Move.flavor_text = relationship(MoveFlavorText,
    order_by=MoveFlavorText.version_group_id, backref='move')
Move.generation = relationship(Generation,
    innerjoin=True,
    backref='moves')
# XXX should this be a dict mapping version group to number?
Move.machines = relationship(Machine,
    backref='move')
Move.meta = relationship(MoveMeta,
    uselist=False,
    backref='move')
Move.meta_stat_changes = relationship(MoveMetaStatChange)
Move.move_effect = relationship(MoveEffect,
    innerjoin=True,
    backref='moves')
Move.move_flags = relationship(MoveFlagMap,
    backref='move')
Move.super_contest_effect = relationship(SuperContestEffect,
    backref='moves')
Move.super_contest_combo_next = association_proxy('super_contest_combo_first', 'second')
Move.super_contest_combo_prev = association_proxy('super_contest_combo_second', 'first')
Move.target = relationship(MoveTarget,
    innerjoin=True,
    backref='moves')
Move.type = relationship(Type,
    innerjoin=True, lazy='joined',
    backref='moves')

Move.effect = markdown.MoveEffectProperty('effect')
Move.effect_map = markdown.MoveEffectPropertyMap('effect_map')
Move.short_effect = markdown.MoveEffectProperty('short_effect')
Move.short_effect_map = markdown.MoveEffectPropertyMap('short_effect_map')

MoveChangelog.changed_in = relationship(VersionGroup,
    innerjoin=True, lazy='joined',
    backref='move_changelog')
MoveChangelog.move_effect = relationship(MoveEffect,
    backref='move_changelog')
MoveChangelog.target = relationship(MoveTarget,
    backref='move_changelog')
MoveChangelog.type = relationship(Type,
    backref='move_changelog')

MoveChangelog.effect = markdown.MoveEffectProperty('effect')
MoveChangelog.effect_map = markdown.MoveEffectPropertyMap('effect_map')
MoveChangelog.short_effect = markdown.MoveEffectProperty('short_effect')
MoveChangelog.short_effect_map = markdown.MoveEffectPropertyMap('short_effect_map')

MoveEffect.changelog = relationship(MoveEffectChangelog,
    order_by=MoveEffectChangelog.changed_in_version_group_id.desc(),
    backref='move_effect')

MoveEffectChangelog.changed_in = relationship(VersionGroup,
    innerjoin=True, lazy='joined',
    backref='move_effect_changelog')

MoveFlagMap.flag = relationship(MoveFlag, innerjoin=True, lazy='joined')

MoveFlavorText.version_group = relationship(VersionGroup,
    innerjoin=True, lazy='joined')
MoveFlavorText.language = relationship(Language,
    innerjoin=True, lazy='joined')

MoveMeta.category = relationship(MoveMetaCategory,
    innerjoin=True, lazy='joined',
    backref='move_meta')
MoveMeta.ailment = relationship(MoveMetaAilment,
    innerjoin=True, lazy='joined',
    backref='move_meta')

MoveMetaStatChange.stat = relationship(Stat,
    innerjoin=True, lazy='joined',
    backref='move_meta_stat_changes')


Nature.decreased_stat = relationship(Stat,
    primaryjoin=Nature.decreased_stat_id==Stat.id,
    innerjoin=True,
    backref='decreasing_natures')
Nature.increased_stat = relationship(Stat,
    primaryjoin=Nature.increased_stat_id==Stat.id,
    innerjoin=True,
    backref='increasing_natures')
Nature.hates_flavor = relationship(ContestType,
    primaryjoin=Nature.hates_flavor_id==ContestType.id,
    innerjoin=True,
    backref='hating_natures')
Nature.likes_flavor = relationship(ContestType,
    primaryjoin=Nature.likes_flavor_id==ContestType.id,
    innerjoin=True,
    backref='liking_natures')
Nature.battle_style_preferences = relationship(NatureBattleStylePreference,
    order_by=NatureBattleStylePreference.move_battle_style_id.asc(),
    backref='nature')
Nature.pokeathlon_effects = relationship(NaturePokeathlonStat,
    order_by=NaturePokeathlonStat.pokeathlon_stat_id.asc())

NatureBattleStylePreference.battle_style = relationship(MoveBattleStyle,
    innerjoin=True, lazy='joined',
    backref='nature_preferences')

NaturePokeathlonStat.pokeathlon_stat = relationship(PokeathlonStat,
    innerjoin=True, lazy='joined',
    backref='nature_effects')


PalPark.area = relationship(PalParkArea,
    innerjoin=True, lazy='joined')


Pokedex.region = relationship(Region,
    innerjoin=True,
    backref='pokedexes')
Pokedex.version_groups = relationship(VersionGroup,
    secondary=PokedexVersionGroup.__table__,
    innerjoin=True,
    order_by=VersionGroup.order.asc(),
    backref='pokedexes')


Pokemon.all_abilities = relationship(Ability,
    secondary=PokemonAbility.__table__,
    order_by=PokemonAbility.slot.asc(),
    backref=backref('all_pokemon', order_by=Pokemon.order.asc()),

Pokemon.abilities = relationship(Ability,
    secondary=PokemonAbility.__table__,
    primaryjoin=and_(
        Pokemon.id == PokemonAbility.pokemon_id,
        PokemonAbility.is_hidden == False,
    ),
    order_by=PokemonAbility.slot.asc(),
    backref=backref('pokemon', order_by=Pokemon.order.asc()),

Pokemon.hidden_ability = relationship(Ability,
    secondary=PokemonAbility.__table__,
    primaryjoin=and_(
        Pokemon.id == PokemonAbility.pokemon_id,
        PokemonAbility.is_hidden == True,
    ),
    uselist=False,
    backref=backref('hidden_pokemon', order_by=Pokemon.order),

Pokemon.pokemon_abilities = relationship(PokemonAbility,
    order_by=PokemonAbility.slot.asc(),
    backref=backref('pokemon', order_by=Pokemon.order.asc()),

Pokemon.forms = relationship(PokemonForm,
    primaryjoin=Pokemon.id==PokemonForm.pokemon_id,
    order_by=(PokemonForm.order.asc(), PokemonForm.form_identifier.asc()),
    lazy='joined')
Pokemon.default_form = relationship(PokemonForm,
    primaryjoin=and_(
        Pokemon.id==PokemonForm.pokemon_id,
        PokemonForm.is_default==True),
    uselist=False, lazy='joined',

Pokemon.items = relationship(PokemonItem,
    backref='pokemon',
    order_by=PokemonItem.rarity.desc(),

Pokemon.stats = relationship(PokemonStat,
    order_by=PokemonStat.stat_id.asc(),
    backref='pokemon')
Pokemon.species = relationship(PokemonSpecies,
    innerjoin=True,
    backref='pokemon')
Pokemon.types = relationship(Type,
    secondary=PokemonType.__table__,
    innerjoin=True, lazy='joined',
    order_by=PokemonType.slot.asc(),
    backref=backref('pokemon', order_by=Pokemon.order))

PokemonAbility.ability = relationship(Ability,
    innerjoin=True)

PokemonDexNumber.pokedex = relationship(Pokedex,
    innerjoin=True, lazy='joined')

PokemonEvolution.trigger = relationship(EvolutionTrigger,
    innerjoin=True, lazy='joined',
    backref='evolutions')
PokemonEvolution.trigger_item = relationship(Item,
    primaryjoin=PokemonEvolution.trigger_item_id==Item.id,
    backref='triggered_evolutions')
PokemonEvolution.held_item = relationship(Item,
    primaryjoin=PokemonEvolution.held_item_id==Item.id,
    backref='required_for_evolutions')
PokemonEvolution.location = relationship(Location,
    backref='triggered_evolutions')
PokemonEvolution.known_move = relationship(Move,
    backref='triggered_evolutions')
PokemonEvolution.known_move_type = relationship(Type,
    primaryjoin=PokemonEvolution.known_move_type_id==Type.id)
PokemonEvolution.party_species = relationship(PokemonSpecies,
    primaryjoin=PokemonEvolution.party_species_id==PokemonSpecies.id,
    backref='triggered_evolutions')
PokemonEvolution.party_type = relationship(Type,
    primaryjoin=PokemonEvolution.party_type_id==Type.id)
PokemonEvolution.trade_species = relationship(PokemonSpecies,
    primaryjoin=PokemonEvolution.trade_species_id==PokemonSpecies.id)
PokemonEvolution.gender = relationship(Gender,
    backref='required_for_evolutions')

PokemonForm.pokemon = relationship(Pokemon,
    primaryjoin=PokemonForm.pokemon_id==Pokemon.id,
    innerjoin=True, lazy='joined')
PokemonForm.species = association_proxy('pokemon', 'species')
PokemonForm.version_group = relationship(VersionGroup,
    innerjoin=True)
PokemonForm.pokeathlon_stats = relationship(PokemonFormPokeathlonStat,
    order_by=PokemonFormPokeathlonStat.pokeathlon_stat_id,
    backref='pokemon_form')

PokemonFormPokeathlonStat.pokeathlon_stat = relationship(PokeathlonStat,
    innerjoin=True, lazy='joined')

PokemonFormGeneration.form = relationship(PokemonForm,
    backref=backref('pokemon_form_generations',
        order_by=PokemonFormGeneration.generation_id))
PokemonFormGeneration.generation = relationship(Generation,
    backref=backref('pokemon_form_generations',
        order_by=PokemonFormGeneration.game_index))

PokemonItem.item = relationship(Item,
    innerjoin=True, lazy='joined',
    backref='pokemon')
PokemonItem.version = relationship(Version,
    innerjoin=True, lazy='joined')

PokemonMove.pokemon = relationship(Pokemon,
    innerjoin=True, lazy='joined',
    backref='pokemon_moves')
PokemonMove.version_group = relationship(VersionGroup,
    innerjoin=True, lazy='joined',
    backref='pokemon_moves')
PokemonMove.machine = relationship(Machine,
    primaryjoin=and_(
        Machine.version_group_id==PokemonMove.version_group_id,
        Machine.move_id==PokemonMove.move_id),
    foreign_keys=[Machine.version_group_id, Machine.move_id],
    uselist=False,
    backref='pokemon_moves')
PokemonMove.move = relationship(Move,
    innerjoin=True, lazy='joined',
    backref='pokemon_moves')
PokemonMove.method = relationship(PokemonMoveMethod,
    innerjoin=True, lazy='joined')

PokemonStat.stat = relationship(Stat,
    innerjoin=True, lazy='joined')

PokemonSpecies.parent_species = relationship(PokemonSpecies,
    primaryjoin=PokemonSpecies.evolves_from_species_id==PokemonSpecies.id,
    remote_side=[PokemonSpecies.id],
    backref=backref('child_species',


PokemonSpecies.evolutions = relationship(PokemonEvolution,
    primaryjoin=PokemonSpecies.id==PokemonEvolution.evolved_species_id,
    backref=backref('evolved_species', innerjoin=True, lazy='joined'))
PokemonSpecies.flavor_text = relationship(PokemonSpeciesFlavorText,
    order_by=PokemonSpeciesFlavorText.version_id.asc(),
    backref='species')
PokemonSpecies.growth_rate = relationship(GrowthRate,
    innerjoin=True,
    backref='species')
PokemonSpecies.habitat = relationship(PokemonHabitat,
    backref='species')
PokemonSpecies.color = relationship(PokemonColor,
    innerjoin=True,
    backref='species')
PokemonSpecies.egg_groups = relationship(EggGroup,
    secondary=PokemonEggGroup.__table__,
    order_by=PokemonEggGroup.egg_group_id.asc(),
    backref=backref('species', order_by=PokemonSpecies.order.asc()))
PokemonSpecies.forms = relationship(PokemonForm,
    secondary=Pokemon.__table__,
    primaryjoin=PokemonSpecies.id==Pokemon.species_id,
    secondaryjoin=Pokemon.id==PokemonForm.pokemon_id,
    order_by=(PokemonForm.order.asc(), PokemonForm.form_identifier.asc()))
PokemonSpecies.default_form = relationship(PokemonForm,
    secondary=Pokemon.__table__,
    primaryjoin=and_(PokemonSpecies.id==Pokemon.species_id,
            Pokemon.is_default==True),
    secondaryjoin=and_(Pokemon.id==PokemonForm.pokemon_id,
            PokemonForm.is_default==True),
    uselist=False,

PokemonSpecies.default_pokemon = relationship(Pokemon,
    primaryjoin=and_(
        PokemonSpecies.id==Pokemon.species_id,
        Pokemon.is_default==True),
    uselist=False, lazy='joined')
PokemonSpecies.evolution_chain = relationship(EvolutionChain,
    backref=backref('species', order_by=PokemonSpecies.id.asc()))
PokemonSpecies.dex_numbers = relationship(PokemonDexNumber,
    innerjoin=True,
    order_by=PokemonDexNumber.pokedex_id.asc(),
    backref='species')
PokemonSpecies.generation = relationship(Generation,
    innerjoin=True,
    backref='species')
PokemonSpecies.shape = relationship(PokemonShape,
    innerjoin=False,
    backref='species')
PokemonSpecies.pal_park = relationship(PalPark,
    uselist=False,
    backref='species')

PokemonSpecies.conquest_abilities = relationship(Ability,
    secondary=ConquestPokemonAbility.__table__,
    order_by=ConquestPokemonAbility.slot,
    backref=backref('conquest_pokemon', order_by=PokemonSpecies.conquest_order,
                    innerjoin=True))
PokemonSpecies.conquest_move = relationship(Move,
    secondary=ConquestPokemonMove.__table__,
    uselist=False,
    backref=backref('conquest_pokemon', order_by=PokemonSpecies.conquest_order))
PokemonSpecies.conquest_evolution = relationship(ConquestPokemonEvolution,
    uselist=False,
    backref=backref('evolved_species', innerjoin=True, lazy='joined', uselist=False))

PokemonSpeciesFlavorText.version = relationship(Version, innerjoin=True, lazy='joined')
PokemonSpeciesFlavorText.language = relationship(Language, innerjoin=True, lazy='joined')

Region.generation = relationship(Generation, uselist=False)
Region.version_group_regions = relationship(VersionGroupRegion,
    order_by=VersionGroupRegion.version_group_id.asc(),
    backref='region')
Region.version_groups = relationship(VersionGroup,
    secondary=VersionGroupRegion.__table__,
    order_by=VersionGroup.order)


Stat.damage_class = relationship(MoveDamageClass,
    backref='stats')


SuperContestCombo.first = relationship(Move,
    primaryjoin=SuperContestCombo.first_move_id==Move.id,
    innerjoin=True, lazy='joined',
    backref='super_contest_combo_first')
SuperContestCombo.second = relationship(Move,
    primaryjoin=SuperContestCombo.second_move_id==Move.id,
    innerjoin=True, lazy='joined',
    backref='super_contest_combo_second')


Type.damage_efficacies = relationship(TypeEfficacy,
    primaryjoin=Type.id==TypeEfficacy.damage_type_id,
    backref=backref('damage_type', innerjoin=True, lazy='joined'),

Type.target_efficacies = relationship(TypeEfficacy,
    primaryjoin=Type.id==TypeEfficacy.target_type_id,
    backref=backref('target_type', innerjoin=True, lazy='joined'),


Type.generation = relationship(Generation,
    innerjoin=True,
    backref='types')
Type.damage_class = relationship(MoveDamageClass,
    backref='types')

TypeGameIndex.type = relationship(Type,
    innerjoin=True, lazy='joined',
    backref='game_indices')
TypeGameIndex.generation = relationship(Generation,
    innerjoin=True, lazy='joined')


Version.generation = association_proxy('version_group', 'generation')

VersionGroup.versions = relationship(Version,
    innerjoin=True,
    order_by=Version.id,
    backref=backref('version_group', lazy='joined'))
VersionGroup.generation = relationship(Generation,
    innerjoin=True, lazy='joined',
    backref=backref('version_groups', order_by=VersionGroup.order))
VersionGroup.version_group_regions = relationship(VersionGroupRegion,
    backref='version_group')
VersionGroup.regions = association_proxy('version_group_regions', 'region')
VersionGroup.pokemon_move_methods = relationship(PokemonMoveMethod,
    secondary=VersionGroupPokemonMoveMethod.__table__,
    primaryjoin=and_(VersionGroup.id == VersionGroupPokemonMoveMethod.version_group_id),
    secondaryjoin=and_(PokemonMoveMethod.id == VersionGroupPokemonMoveMethod.pokemon_move_method_id),
    backref="version_groups")
VersionGroup.machines = relationship(Machine,
    innerjoin=True,
    order_by=Machine.machine_number)


VersionGroupPokemonMoveMethod.version_group = relationship(VersionGroup,
    backref='version_group_move_methods')
VersionGroupPokemonMoveMethod.pokemon_move_method = relationship(PokemonMoveMethod,
    backref='version_group_move_methods')

