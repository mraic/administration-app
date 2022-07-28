import random

import click
from flask.cli import with_appcontext


@click.group(
    name="db_migrations",
)
def db_migrations():
    pass


@db_migrations.command("test")
@with_appcontext
def db_migrations_test():
    print("This is a test")


@db_migrations.command("regular_data")
@with_appcontext
def regular_data():
    from src import List, ListItem

    list_1 = List(
        name="Stanje_artikla",
        description="Stanje_artikla",
    )

    list_1.add()
    list_1.commit_or_rollback()

    list_item_1 = ListItem(
        id='737da853-e96a-4f38-8be8-37f7c1c2c0c9',
        name="Novo",
        description="Novo",
        list_id=list_1.id
    )
    list_item_1.add()
    list_item_1.commit_or_rollback()

    list_item_2 = ListItem(
        name="Korišteno",
        description="Korišteno",
        list_id=list_1.id
    )
    list_item_2.add()
    list_item_2.commit_or_rollback()

    print("Lista stanje_artikla uspiješno dodana")
    return list_item_1, list_item_2


@db_migrations.command("fake_data")
@with_appcontext
def fake_data():
    from src import ListItem
    category_list_id = []
    subcategory_list = []
    list_items_id = []

    itemi = ListItem.query.with_entities(ListItem.id).all()
    for i in range(len(itemi)):
        list_items_id.append(str(itemi[i][0]))

    from src import Category, Subcategory, Item
    from faker import Faker
    fake = Faker()

    for i in range(500):
        category = Category(
            name=fake.pystr(max_chars=5),
            category_icon="AddTask"
        )

        category.add()
        category.commit_or_rollback()

        category_list_id.append(category.id)

        categorija_id = random.choice(category_list_id)

        subcategory = Subcategory(
            name=fake.pystr(max_chars=9),
            subcategory_icon="test",
            category_id=categorija_id
        )

        subcategory.add()
        subcategory.commit_or_rollback()

        subcategory_list.append(subcategory)

        listaitema = random.choice(list_items_id)

        sub_category_obj = subcategory_list[
            random.randint(0, len(subcategory_list) -1)]

        items = Item(
            name=fake.pystr(max_chars=5),
            description=fake.pystr(min_chars=20),
            price=fake.unique.random_int(min=1, max=999),
            condition_id=listaitema,
            subcategory_id=sub_category_obj.id,
            category_id=sub_category_obj.category_id
        )
        items.add()
        items.commit_or_rollback()
