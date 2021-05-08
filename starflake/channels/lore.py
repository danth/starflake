import itertools

from starflake.channels import DocumentChannel
from starflake.game_objects import BondingException
from starflake.game_objects.molecule import Molecule
from starflake.game_objects.constants import TABLE_GROUPS, TABLE_PERIODS, COLOURS


def make_example_compound(periodic_table, size):
    """Select a group of elements which are able to bond."""

    # Search through all possible pairs of elements
    for combination in itertools.combinations(periodic_table.elements, size):
        try:
            molecules = [Molecule([element]) for element in combination]
            compound = Molecule.bond_many(molecules)
        except BondingException:
            continue
        else:
            # Bonding succeeded, therefore we have found a valid molecule
            return combination, compound


class LoreChannel(DocumentChannel):
    """A document containing basic information about how to play."""

    name = "lore"
    topic = "This channel contains information about Starflake's chemistry system."

    async def send_document(self, messageable):
        await messageable.send(
            f"There are {TABLE_GROUPS * TABLE_PERIODS} chemical elements in Starflake. "
            "Similarly to real life, they can be written in a periodic table:"
        )
        await self.game.periodic_table.send_embed(messageable)

        await messageable.send(
            "However, the formation of compounds is different. Rather than using "
            "electrons to bond, each element has a spectrum containing up to "
            f"{len(COLOURS)} coloured spots."
        )

        elements, compound = make_example_compound(self.game.periodic_table, 2)
        await elements[0].send_embed(messageable)
        await messageable.send(
            "The number of colours per element increases with each new period. "
            "Here is another element:"
        )
        await elements[1].send_embed(messageable)
        await messageable.send(
            "If any colour is present in both spectra, the elements can't bond. "
            f"{elements[0].name.title()} and {elements[1].name} have no overlapping "
            f"colours, so they will react to form {compound.name}:"
        )
        await compound.send_embed(messageable)
        await messageable.send(
            "The spectrum of the new compound contains every colour from its "
            f"constituent atoms. Once a compound has all {len(COLOURS)} colours, "
            "it can't gain any more bonds."
        )

        elements, compound = make_example_compound(self.game.periodic_table, 3)
        await messageable.send(
            "Of course, molecules can contain more than two elements - reacting "
            f"{elements[0].name}, {elements[1].name} and {elements[2].name} produces:"
        )
        await compound.send_embed(messageable)

        heaviest_element = self.game.periodic_table.elements[-1]
        await messageable.send(
            "Heavier molecules have a stronger attractive force, so during a reaction "
            "they will bond before lighter molecules. When reading the periodic table "
            "from left to right, each element has a mass number of one more than the "
            f"previous element. {heaviest_element.name.title()} is the heaviest - "
            f"its relative mass is {heaviest_element.mass}."
        )
        await heaviest_element.send_embed(messageable)
