create table budget(
	codename varchar(255) primary key,
	daily_limit integer
);

create table category(
	codename varchar(255) primary key,
	name varchar(255),
	is_base_expense boolean,
	aliases text
);

create table expense(
	id integer primary key,
	amount integer,
	created datetime,
	category_codename integer,
	raw_text text,
	FOREIGN KEY(category_codename) REFERENCES category(codename)
);

insert into category (codename, name, is_base_expense, aliases)
values
	("products", "food", true, ""),
	("coffee", "coffee", true, ""),
	("dinner", "lunch", true, "bl,  business lunch"),
	("cafe", "lounge", true, "restaurant, rest, mac, McDonald's, mcduck, kfc, ilpatio, il patio"),
	("transport", "public transport", false, "metro, bus, trolleybus"),
	("taxi", "uber", false, "yandex, yandex taxi"),
	("phone", "mts ", false, "tele2, connection"),
	("books", "book", false, "literature, lit"),
	("internet", "inet", false, ""),
	("subscriptions", "subscription", false, ""),
	("other", "others", true, "");

insert into budget(codename, daily_limit) values ('base', 500);
