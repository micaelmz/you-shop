create table main.product
(
    id          integer                                                       not null
        constraint id
            primary key autoincrement,
    name        TEXT                                                          not null,
    price_new   REAL                                                          not null,
    price_old   REAL    default 0                                             not null,
    category    integer                                                       not null,
    promotion   integer default 0                                             not null,
    img_url     TEXT    default 'https://demofree.sirv.com/nope-not-here.jpg' not null,
    description TEXT,
    color       TEXT,
    information TEXT,
    extra_Img   TEXT
);


create table main.review
(
    id          integer          not null
        constraint review_pk
            primary key autoincrement,
    author_id   integer          not null,
    product_id  integer          not null,
    content     TEXT,
    grade       REAL default 0.0 not null,
    date        TEXT             not null,
    author_name TEXT,
    constraint date_check
        check (date LIKE '__-__-____')
);
