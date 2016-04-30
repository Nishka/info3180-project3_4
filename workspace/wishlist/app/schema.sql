if not exists wishlist_users create table wishlist_users
{
    id integer primary key autoincrement,
    firstname text not null,
    lastname text not null,
    email text not null,
    password text not null
}

if not exists wishlist_set create table wishlist_set
{
    list_id integer primary key autoincrement,
    id integer,
    title text not null,
    description text,
    url text not null,
    thumbnail text not null
}