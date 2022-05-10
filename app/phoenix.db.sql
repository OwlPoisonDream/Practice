BEGIN TRANSACTION;
CREATE TABLE IF NOT EXISTS "users" (
	"id"	INTEGER NOT NULL,
	"email"	VARCHAR(20) NOT NULL,
	"password_hash"	VARCHAR(100) NOT NULL,
	"who"	INTEGER,
	PRIMARY KEY("id")
);
CREATE TABLE IF NOT EXISTS "projects" (
	"id"	INTEGER NOT NULL,
	"projectName"	VARCHAR(255),
	"descProject"	VARCHAR(255),
	"linkDisk"	VARCHAR(255),
	PRIMARY KEY("id")
);
CREATE TABLE IF NOT EXISTS "user_project" (
	"id"	INTEGER NOT NULL,
	"User_id"	INTEGER,
	"Project_id"	INTEGER,
	PRIMARY KEY("id")
);
CREATE TABLE IF NOT EXISTS "documents" (
	"id"	INTEGER NOT NULL,
	"name"	VARCHAR(50),
	"link"	TEXT,
	"UserID"	INTEGER,
	PRIMARY KEY("id")
);
CREATE TABLE IF NOT EXISTS "users_Data" (
	"id"	INTEGER NOT NULL,
	"idUser"	INTEGER,
	"name"	VARCHAR(100),
	"birthDAy"	VARCHAR(100),
	"passport"	VARCHAR(100),
	"passportData"	VARCHAR(100),
	"passportBy"	VARCHAR(100),
	"passportCod"	VARCHAR(100),
	"address"	TEXT,
	"nickname"	VARCHAR(20),
	"link_vk"	VARCHAR(50),
	"inn"	VARCHAR(12),
	"bank_details"	VARCHAR(100),
	"bankName"	VARCHAR(100),
	"phone_number"	VARCHAR(11),
	"bankAccount"	TEXT,
	"tags"	TEXT,
	"avatar"	TEXT,
	PRIMARY KEY("id")
);
CREATE TABLE IF NOT EXISTS "folders" (
	"id"	INTEGER,
	"id_user"	INTEGER,
	"id_progect"	INTEGER,
	"link"	TEXT,
	"name"	TEXT,
	PRIMARY KEY("id")
);
CREATE TABLE IF NOT EXISTS "task" (
	"id"	INTEGER NOT NULL,
	"idUser"	INTEGER,
	"idProject"	INTEGER,
	"nameTask"	VARCHAR(255),
	"descTask"	VARCHAR(255),
	"timeTask"	VARCHAR(255),
	"manyTask"	VARCHAR(255),
	"statusСompleted"	VARCHAR(255),
	"receipt"	FLOAT,
	"linkDisk"	VARCHAR(255),
	"id_folder"	INTEGER,
	PRIMARY KEY("id")
);
INSERT INTO "users" ("id","email","password_hash","who") VALUES (1,'root','pbkdf2:sha256:260000$QjMQQacDv3EbCU9h$6a0ccfcbd6c00b0b55c128bc9b7ab0c25afb773b2415d15e10f6a3baa189a9c4',2),
 (2,'supefish@gmail.com','pbkdf2:sha256:260000$7ANF4T6C1Ilbz4T3$5c2df245530ccc740ecaf4c7354ed835b9795c7fb0fa917d50e4b1f723e4a1bf',1),
 (3,'123@gmail.com','pbkdf2:sha256:260000$nQL9HyjkL5qYy6W8$3360e89e8540a6621a4b8866ae709bd163f750430b729e30b9d8024cbd6dce34',0),
 (4,'lelouchr1377@gmail.com','pbkdf2:sha256:260000$cMvYOdlSgqvD7XXk$52d56820401d15f9f4f9ee5c992f5b3229eb5bb6b60607620b0f7c61a7e62833',0);
INSERT INTO "projects" ("id","projectName","descProject","linkDisk") VALUES (1,'Рисуем комиксы','ты пидр','/Феникс проекты/Рисуем комиксы'),
 (2,'купить пиво','сходить до кб и купить всем поп балтике 9 и сухарей в придачу','/Феникс проекты/купить пиво'),
 (3,'пошел нахуй','— Любя, съешь щипцы, — вздохнёт мэр, — кайф жгуч.  А ещё хорошо бы уметь всем на зависть чётко и наглядно писать буквы и цифры.  Аэрофотосъёмка ландшафта уже выявила земли богачей и процветающих крестьян.  Бегом марш! У месторождения кварцующихся фей без слёз хочется электрическую пыль.  Безмозглый широковещательный цифровой передатчик сужающихся экспонент.  Блеф разъедает ум, чаще цыгана живёшь беспокойно, юля — грех это!  Борец за идею Чучхэ выступил с гиком, шумом, жаром и фырканьем на съезде — и в ящик.  БУКВОПЕЧАТАЮЩЕЙ СВЯЗИ НУЖНЫ ХОРОШИЕ Э/МАГНИТНЫЕ РЕЛЕ. ДАТЬ ЦИФРЫ (1234567890+= .?-)  В чащах юга жил бы цитрус? Да, но фальшивый экземпляр!  Вопрос футбольных энциклопедий замещая чушью: эй, где съеден ёж?  Всё ускоряющаяся эволюция компьютерных технологий предъявила жёсткие требования к производителям как собственно вычислительной техники, так и периферийных устройств.  Вступив в бой с шипящими змеями — эфой и гадюкой, — маленький, цепкий, храбрый ёж съел их.  Государев указ: душегубцев да шваль всякую высечь, да калёным железом по щекам этих физиономий съездить!','/Феникс проекты/пошел нахуй');
INSERT INTO "user_project" ("id","User_id","Project_id") VALUES (1,1,1),
 (2,2,1),
 (3,2,2),
 (4,3,2),
 (5,1,3),
 (6,2,3),
 (7,4,3);
INSERT INTO "users_Data" ("id","idUser","name","birthDAy","passport","passportData","passportBy","passportCod","address","nickname","link_vk","inn","bank_details","bankName","phone_number","bankAccount","tags","avatar") VALUES (1,1,'Админ','2005-03-24','1','11111','111111','11111','адрес','Рыба','13213213213123','772808373000','12233','12313213213','89889988989889','акаунт','[]','static/photos/Админ/64a65926-756e-4bc5-983d-9259af0847e4.jpg'),
 (2,2,'Виктор Бахчеев','1979-08-15','5555 555555','2020-06-22','фвцфцвфцвфцв','770-068','адрес','v.bah','','','','','','аккаунт','[''Менеджер'']','static/photos/Сергей/20220320_145834.jpg'),
 (3,3,'Твоя мама','1999-04-25','1111 111111','sdaf','bfg','12341',NULL,'pogonyalo','none','12354','sdfg234','sdfgr543','65644282454',NULL,'[''Программист'']','static/photos/Твоя мама/cu2pVKurwOc.jpg'),
 (4,4,'Говноед Давид Евревич','2002-01-09','3123213213132','31232132132132','31312323213','31231231232131',NULL,'ГДЗ','vk.com/davidghoul','31323213123123','312321312312312','312312321312','31232312312313321',NULL,NULL,NULL);
INSERT INTO "folders" ("id","id_user","id_progect","link","name") VALUES (1,NULL,1,NULL,'Голые фотки'),
 (2,NULL,2,NULL,'поменять трусы'),
 (3,NULL,2,NULL,'купить пивас'),
 (4,NULL,2,NULL,'поменять трусы'),
 (5,NULL,3,NULL,'купить пивас'),
 (6,NULL,3,NULL,'скушать чебупельку');
INSERT INTO "task" ("id","idUser","idProject","nameTask","descTask","timeTask","manyTask","statusСompleted","receipt","linkDisk","id_folder") VALUES (1,1,1,'Посасать','соси присасывай','2022-05-06','1000','Complete',NULL,'/Феникс проекты/Рисуем комиксы/Админ/Посасать',1),
 (2,2,1,'Посасать','соси присасывай','2022-05-06','1000','Complete',NULL,'/Феникс проекты/Рисуем комиксы/Сергей/Посасать',1),
 (3,2,1,'Посасать2','соси присасывай','2022-05-06','1000','Complete',NULL,'/Феникс проекты/Рисуем комиксы/Сергей/Посасать2',1),
 (4,2,2,'Shido a live','Make Nia fall in love to Shido','2015-12-26','2500','Uncomplete',NULL,NULL,NULL),
 (6,1,2,'купить шарик','Вступив в бой с шипящими змеями — эфой и гадюкой, — маленький, цепкий, храбрый ёж съел их.  Государев указ: душегубцев да шваль всякую высечь, да калёным железом по щекам этих физиономий съездить!  Друг мой эльф! Яшке б свёз птиц южных чащ!  Завершён ежегодный съезд эрудированных школьников, мечтающих глубоко проникнуть в тайны физических явлений и химических реакций.  Здесь фабула объять не может всех эмоций — шепелявый скороход в юбке тащит горячий мёд.  Лингвисты в ужасе: фиг выговоришь этюд: «подъём челябинский, запах щец».  Любя, съешь щипцы, — вздохнёт мэр, — кайф жгуч.  Мюзикл-буфф «Огнедышащий простужается ночью» (в 12345 сценах и 67890 эпизодах).  Обдав его удушающей пылью, множество ярких фаэтонов исчезло из цирка.  Однажды съев фейхоа, я, как зацикленный, ностальгирую всё чаще и больше по этому чуду.  Официально заявляю читающим: даёшь подъем операции Ы! Хуже с ёлкой бог экспериментирует.','2022-05-27','10000000000','Uncomplete',NULL,'/Феникс проекты/Рисуем комиксы/Админ',2),
 (7,2,2,'купить шарик','Вступив в бой с шипящими змеями — эфой и гадюкой, — маленький, цепкий, храбрый ёж съел их.  Государев указ: душегубцев да шваль всякую высечь, да калёным железом по щекам этих физиономий съездить!  Друг мой эльф! Яшке б свёз птиц южных чащ!  Завершён ежегодный съезд эрудированных школьников, мечтающих глубоко проникнуть в тайны физических явлений и химических реакций.  Здесь фабула объять не может всех эмоций — шепелявый скороход в юбке тащит горячий мёд.  Лингвисты в ужасе: фиг выговоришь этюд: «подъём челябинский, запах щец».  Любя, съешь щипцы, — вздохнёт мэр, — кайф жгуч.  Мюзикл-буфф «Огнедышащий простужается ночью» (в 12345 сценах и 67890 эпизодах).  Обдав его удушающей пылью, множество ярких фаэтонов исчезло из цирка.  Однажды съев фейхоа, я, как зацикленный, ностальгирую всё чаще и больше по этому чуду.  Официально заявляю читающим: даёшь подъем операции Ы! Хуже с ёлкой бог экспериментирует.','2022-05-27','10000000000','Uncomplete',NULL,'/Феникс проекты/купить пиво/Сергей',2),
 (8,1,2,'купить шарик','Вступив в бой с шипящими змеями — эфой и гадюкой, — маленький, цепкий, храбрый ёж съел их.  Государев указ: душегубцев да шваль всякую высечь, да калёным железом по щекам этих физиономий съездить!  Друг мой эльф! Яшке б свёз птиц южных чащ!  Завершён ежегодный съезд эрудированных школьников, мечтающих глубоко проникнуть в тайны физических явлений и химических реакций.  Здесь фабула объять не может всех эмоций — шепелявый скороход в юбке тащит горячий мёд.  Лингвисты в ужасе: фиг выговоришь этюд: «подъём челябинский, запах щец».  Любя, съешь щипцы, — вздохнёт мэр, — кайф жгуч.  Мюзикл-буфф «Огнедышащий простужается ночью» (в 12345 сценах и 67890 эпизодах).  Обдав его удушающей пылью, множество ярких фаэтонов исчезло из цирка.  Однажды съев фейхоа, я, как зацикленный, ностальгирую всё чаще и больше по этому чуду.  Официально заявляю читающим: даёшь подъем операции Ы! Хуже с ёлкой бог экспериментирует.','2022-05-27','10000000000','Uncomplete',NULL,'/Феникс проекты/купить пиво/Админ',4),
 (9,2,2,'купить шарик','Вступив в бой с шипящими змеями — эфой и гадюкой, — маленький, цепкий, храбрый ёж съел их.  Государев указ: душегубцев да шваль всякую высечь, да калёным железом по щекам этих физиономий съездить!  Друг мой эльф! Яшке б свёз птиц южных чащ!  Завершён ежегодный съезд эрудированных школьников, мечтающих глубоко проникнуть в тайны физических явлений и химических реакций.  Здесь фабула объять не может всех эмоций — шепелявый скороход в юбке тащит горячий мёд.  Лингвисты в ужасе: фиг выговоришь этюд: «подъём челябинский, запах щец».  Любя, съешь щипцы, — вздохнёт мэр, — кайф жгуч.  Мюзикл-буфф «Огнедышащий простужается ночью» (в 12345 сценах и 67890 эпизодах).  Обдав его удушающей пылью, множество ярких фаэтонов исчезло из цирка.  Однажды съев фейхоа, я, как зацикленный, ностальгирую всё чаще и больше по этому чуду.  Официально заявляю читающим: даёшь подъем операции Ы! Хуже с ёлкой бог экспериментирует.','2022-05-27','10000000000','Uncomplete',NULL,'/Феникс проекты/купить пиво/Сергей',4),
 (10,4,2,'купить шарик','Вступив в бой с шипящими змеями — эфой и гадюкой, — маленький, цепкий, храбрый ёж съел их.  Государев указ: душегубцев да шваль всякую высечь, да калёным железом по щекам этих физиономий съездить!  Друг мой эльф! Яшке б свёз птиц южных чащ!  Завершён ежегодный съезд эрудированных школьников, мечтающих глубоко проникнуть в тайны физических явлений и химических реакций.  Здесь фабула объять не может всех эмоций — шепелявый скороход в юбке тащит горячий мёд.  Лингвисты в ужасе: фиг выговоришь этюд: «подъём челябинский, запах щец».  Любя, съешь щипцы, — вздохнёт мэр, — кайф жгуч.  Мюзикл-буфф «Огнедышащий простужается ночью» (в 12345 сценах и 67890 эпизодах).  Обдав его удушающей пылью, множество ярких фаэтонов исчезло из цирка.  Однажды съев фейхоа, я, как зацикленный, ностальгирую всё чаще и больше по этому чуду.  Официально заявляю читающим: даёшь подъем операции Ы! Хуже с ёлкой бог экспериментирует.','2022-05-27','10000000000','Uncomplete',NULL,'/Феникс проекты/купить пиво/Говноед Давид Евревич',4),
 (11,1,2,'купить шарик','Вступив в бой с шипящими змеями — эфой и гадюкой, — маленький, цепкий, храбрый ёж съел их.  Государев указ: душегубцев да шваль всякую высечь, да калёным железом по щекам этих физиономий съездить!  Друг мой эльф! Яшке б свёз птиц южных чащ!  Завершён ежегодный съезд эрудированных школьников, мечтающих глубоко проникнуть в тайны физических явлений и химических реакций.  Здесь фабула объять не может всех эмоций — шепелявый скороход в юбке тащит горячий мёд.  Лингвисты в ужасе: фиг выговоришь этюд: «подъём челябинский, запах щец».  Любя, съешь щипцы, — вздохнёт мэр, — кайф жгуч.  Мюзикл-буфф «Огнедышащий простужается ночью» (в 12345 сценах и 67890 эпизодах).  Обдав его удушающей пылью, множество ярких фаэтонов исчезло из цирка.  Однажды съев фейхоа, я, как зацикленный, ностальгирую всё чаще и больше по этому чуду.  Официально заявляю читающим: даёшь подъем операции Ы! Хуже с ёлкой бог экспериментирует.','2022-05-27','10000000000','Uncomplete',NULL,'/Феникс проекты/купить пиво/Админ',4),
 (12,2,2,'купить шарик','Вступив в бой с шипящими змеями — эфой и гадюкой, — маленький, цепкий, храбрый ёж съел их.  Государев указ: душегубцев да шваль всякую высечь, да калёным железом по щекам этих физиономий съездить!  Друг мой эльф! Яшке б свёз птиц южных чащ!  Завершён ежегодный съезд эрудированных школьников, мечтающих глубоко проникнуть в тайны физических явлений и химических реакций.  Здесь фабула объять не может всех эмоций — шепелявый скороход в юбке тащит горячий мёд.  Лингвисты в ужасе: фиг выговоришь этюд: «подъём челябинский, запах щец».  Любя, съешь щипцы, — вздохнёт мэр, — кайф жгуч.  Мюзикл-буфф «Огнедышащий простужается ночью» (в 12345 сценах и 67890 эпизодах).  Обдав его удушающей пылью, множество ярких фаэтонов исчезло из цирка.  Однажды съев фейхоа, я, как зацикленный, ностальгирую всё чаще и больше по этому чуду.  Официально заявляю читающим: даёшь подъем операции Ы! Хуже с ёлкой бог экспериментирует.','2022-05-27','10000000000','Uncomplete',NULL,'/Феникс проекты/купить пиво/Сергей',4),
 (13,4,2,'купить шарик','Вступив в бой с шипящими змеями — эфой и гадюкой, — маленький, цепкий, храбрый ёж съел их.  Государев указ: душегубцев да шваль всякую высечь, да калёным железом по щекам этих физиономий съездить!  Друг мой эльф! Яшке б свёз птиц южных чащ!  Завершён ежегодный съезд эрудированных школьников, мечтающих глубоко проникнуть в тайны физических явлений и химических реакций.  Здесь фабула объять не может всех эмоций — шепелявый скороход в юбке тащит горячий мёд.  Лингвисты в ужасе: фиг выговоришь этюд: «подъём челябинский, запах щец».  Любя, съешь щипцы, — вздохнёт мэр, — кайф жгуч.  Мюзикл-буфф «Огнедышащий простужается ночью» (в 12345 сценах и 67890 эпизодах).  Обдав его удушающей пылью, множество ярких фаэтонов исчезло из цирка.  Однажды съев фейхоа, я, как зацикленный, ностальгирую всё чаще и больше по этому чуду.  Официально заявляю читающим: даёшь подъем операции Ы! Хуже с ёлкой бог экспериментирует.','2022-05-27','10000000000','Uncomplete',NULL,'/Феникс проекты/купить пиво/Говноед Давид Евревич',4),
 (14,1,2,'купить шарик','Вступив в бой с шипящими змеями — эфой и гадюкой, — маленький, цепкий, храбрый ёж съел их.  Государев указ: душегубцев да шваль всякую высечь, да калёным железом по щекам этих физиономий съездить!  Друг мой эльф! Яшке б свёз птиц южных чащ!  Завершён ежегодный съезд эрудированных школьников, мечтающих глубоко проникнуть в тайны физических явлений и химических реакций.  Здесь фабула объять не может всех эмоций — шепелявый скороход в юбке тащит горячий мёд.  Лингвисты в ужасе: фиг выговоришь этюд: «подъём челябинский, запах щец».  Любя, съешь щипцы, — вздохнёт мэр, — кайф жгуч.  Мюзикл-буфф «Огнедышащий простужается ночью» (в 12345 сценах и 67890 эпизодах).  Обдав его удушающей пылью, множество ярких фаэтонов исчезло из цирка.  Однажды съев фейхоа, я, как зацикленный, ностальгирую всё чаще и больше по этому чуду.  Официально заявляю читающим: даёшь подъем операции Ы! Хуже с ёлкой бог экспериментирует.','2022-05-27','10000000000','Uncomplete',NULL,'/Феникс проекты/купить пиво/Админ',4),
 (15,2,2,'купить шарик','Вступив в бой с шипящими змеями — эфой и гадюкой, — маленький, цепкий, храбрый ёж съел их.  Государев указ: душегубцев да шваль всякую высечь, да калёным железом по щекам этих физиономий съездить!  Друг мой эльф! Яшке б свёз птиц южных чащ!  Завершён ежегодный съезд эрудированных школьников, мечтающих глубоко проникнуть в тайны физических явлений и химических реакций.  Здесь фабула объять не может всех эмоций — шепелявый скороход в юбке тащит горячий мёд.  Лингвисты в ужасе: фиг выговоришь этюд: «подъём челябинский, запах щец».  Любя, съешь щипцы, — вздохнёт мэр, — кайф жгуч.  Мюзикл-буфф «Огнедышащий простужается ночью» (в 12345 сценах и 67890 эпизодах).  Обдав его удушающей пылью, множество ярких фаэтонов исчезло из цирка.  Однажды съев фейхоа, я, как зацикленный, ностальгирую всё чаще и больше по этому чуду.  Официально заявляю читающим: даёшь подъем операции Ы! Хуже с ёлкой бог экспериментирует.','2022-05-27','10000000000','Uncomplete',NULL,'/Феникс проекты/купить пиво/Сергей',4),
 (16,4,2,'купить шарик','Вступив в бой с шипящими змеями — эфой и гадюкой, — маленький, цепкий, храбрый ёж съел их.  Государев указ: душегубцев да шваль всякую высечь, да калёным железом по щекам этих физиономий съездить!  Друг мой эльф! Яшке б свёз птиц южных чащ!  Завершён ежегодный съезд эрудированных школьников, мечтающих глубоко проникнуть в тайны физических явлений и химических реакций.  Здесь фабула объять не может всех эмоций — шепелявый скороход в юбке тащит горячий мёд.  Лингвисты в ужасе: фиг выговоришь этюд: «подъём челябинский, запах щец».  Любя, съешь щипцы, — вздохнёт мэр, — кайф жгуч.  Мюзикл-буфф «Огнедышащий простужается ночью» (в 12345 сценах и 67890 эпизодах).  Обдав его удушающей пылью, множество ярких фаэтонов исчезло из цирка.  Однажды съев фейхоа, я, как зацикленный, ностальгирую всё чаще и больше по этому чуду.  Официально заявляю читающим: даёшь подъем операции Ы! Хуже с ёлкой бог экспериментирует.','2022-05-27','10000000000','Uncomplete',NULL,'/Феникс проекты/купить пиво/Говноед Давид Евревич',4),
 (17,1,2,'купить шарик','Вступив в бой с шипящими змеями — эфой и гадюкой, — маленький, цепкий, храбрый ёж съел их.  Государев указ: душегубцев да шваль всякую высечь, да калёным железом по щекам этих физиономий съездить!  Друг мой эльф! Яшке б свёз птиц южных чащ!  Завершён ежегодный съезд эрудированных школьников, мечтающих глубоко проникнуть в тайны физических явлений и химических реакций.  Здесь фабула объять не может всех эмоций — шепелявый скороход в юбке тащит горячий мёд.  Лингвисты в ужасе: фиг выговоришь этюд: «подъём челябинский, запах щец».  Любя, съешь щипцы, — вздохнёт мэр, — кайф жгуч.  Мюзикл-буфф «Огнедышащий простужается ночью» (в 12345 сценах и 67890 эпизодах).  Обдав его удушающей пылью, множество ярких фаэтонов исчезло из цирка.  Однажды съев фейхоа, я, как зацикленный, ностальгирую всё чаще и больше по этому чуду.  Официально заявляю читающим: даёшь подъем операции Ы! Хуже с ёлкой бог экспериментирует.','2022-05-27','10000000000','Uncomplete',NULL,'/Феникс проекты/купить пиво/Админ',4),
 (18,2,2,'купить шарик','Вступив в бой с шипящими змеями — эфой и гадюкой, — маленький, цепкий, храбрый ёж съел их.  Государев указ: душегубцев да шваль всякую высечь, да калёным железом по щекам этих физиономий съездить!  Друг мой эльф! Яшке б свёз птиц южных чащ!  Завершён ежегодный съезд эрудированных школьников, мечтающих глубоко проникнуть в тайны физических явлений и химических реакций.  Здесь фабула объять не может всех эмоций — шепелявый скороход в юбке тащит горячий мёд.  Лингвисты в ужасе: фиг выговоришь этюд: «подъём челябинский, запах щец».  Любя, съешь щипцы, — вздохнёт мэр, — кайф жгуч.  Мюзикл-буфф «Огнедышащий простужается ночью» (в 12345 сценах и 67890 эпизодах).  Обдав его удушающей пылью, множество ярких фаэтонов исчезло из цирка.  Однажды съев фейхоа, я, как зацикленный, ностальгирую всё чаще и больше по этому чуду.  Официально заявляю читающим: даёшь подъем операции Ы! Хуже с ёлкой бог экспериментирует.','2022-05-27','10000000000','Uncomplete',NULL,'/Феникс проекты/купить пиво/Сергей',4),
 (19,4,2,'купить шарик','Вступив в бой с шипящими змеями — эфой и гадюкой, — маленький, цепкий, храбрый ёж съел их.  Государев указ: душегубцев да шваль всякую высечь, да калёным железом по щекам этих физиономий съездить!  Друг мой эльф! Яшке б свёз птиц южных чащ!  Завершён ежегодный съезд эрудированных школьников, мечтающих глубоко проникнуть в тайны физических явлений и химических реакций.  Здесь фабула объять не может всех эмоций — шепелявый скороход в юбке тащит горячий мёд.  Лингвисты в ужасе: фиг выговоришь этюд: «подъём челябинский, запах щец».  Любя, съешь щипцы, — вздохнёт мэр, — кайф жгуч.  Мюзикл-буфф «Огнедышащий простужается ночью» (в 12345 сценах и 67890 эпизодах).  Обдав его удушающей пылью, множество ярких фаэтонов исчезло из цирка.  Однажды съев фейхоа, я, как зацикленный, ностальгирую всё чаще и больше по этому чуду.  Официально заявляю читающим: даёшь подъем операции Ы! Хуже с ёлкой бог экспериментирует.','2022-05-27','10000000000','Uncomplete',NULL,'/Феникс проекты/купить пиво/Говноед Давид Евревич',4),
 (20,1,2,'купить шарик','Вступив в бой с шипящими змеями — эфой и гадюкой, — маленький, цепкий, храбрый ёж съел их.  Государев указ: душегубцев да шваль всякую высечь, да калёным железом по щекам этих физиономий съездить!  Друг мой эльф! Яшке б свёз птиц южных чащ!  Завершён ежегодный съезд эрудированных школьников, мечтающих глубоко проникнуть в тайны физических явлений и химических реакций.  Здесь фабула объять не может всех эмоций — шепелявый скороход в юбке тащит горячий мёд.  Лингвисты в ужасе: фиг выговоришь этюд: «подъём челябинский, запах щец».  Любя, съешь щипцы, — вздохнёт мэр, — кайф жгуч.  Мюзикл-буфф «Огнедышащий простужается ночью» (в 12345 сценах и 67890 эпизодах).  Обдав его удушающей пылью, множество ярких фаэтонов исчезло из цирка.  Однажды съев фейхоа, я, как зацикленный, ностальгирую всё чаще и больше по этому чуду.  Официально заявляю читающим: даёшь подъем операции Ы! Хуже с ёлкой бог экспериментирует.','2022-05-27','10000000000','Uncomplete',NULL,'/Феникс проекты/купить пиво/Админ',4),
 (21,2,2,'купить шарик','Вступив в бой с шипящими змеями — эфой и гадюкой, — маленький, цепкий, храбрый ёж съел их.  Государев указ: душегубцев да шваль всякую высечь, да калёным железом по щекам этих физиономий съездить!  Друг мой эльф! Яшке б свёз птиц южных чащ!  Завершён ежегодный съезд эрудированных школьников, мечтающих глубоко проникнуть в тайны физических явлений и химических реакций.  Здесь фабула объять не может всех эмоций — шепелявый скороход в юбке тащит горячий мёд.  Лингвисты в ужасе: фиг выговоришь этюд: «подъём челябинский, запах щец».  Любя, съешь щипцы, — вздохнёт мэр, — кайф жгуч.  Мюзикл-буфф «Огнедышащий простужается ночью» (в 12345 сценах и 67890 эпизодах).  Обдав его удушающей пылью, множество ярких фаэтонов исчезло из цирка.  Однажды съев фейхоа, я, как зацикленный, ностальгирую всё чаще и больше по этому чуду.  Официально заявляю читающим: даёшь подъем операции Ы! Хуже с ёлкой бог экспериментирует.','2022-05-27','10000000000','Uncomplete',NULL,'/Феникс проекты/купить пиво/Сергей',4),
 (22,4,2,'купить шарик','Вступив в бой с шипящими змеями — эфой и гадюкой, — маленький, цепкий, храбрый ёж съел их.  Государев указ: душегубцев да шваль всякую высечь, да калёным железом по щекам этих физиономий съездить!  Друг мой эльф! Яшке б свёз птиц южных чащ!  Завершён ежегодный съезд эрудированных школьников, мечтающих глубоко проникнуть в тайны физических явлений и химических реакций.  Здесь фабула объять не может всех эмоций — шепелявый скороход в юбке тащит горячий мёд.  Лингвисты в ужасе: фиг выговоришь этюд: «подъём челябинский, запах щец».  Любя, съешь щипцы, — вздохнёт мэр, — кайф жгуч.  Мюзикл-буфф «Огнедышащий простужается ночью» (в 12345 сценах и 67890 эпизодах).  Обдав его удушающей пылью, множество ярких фаэтонов исчезло из цирка.  Однажды съев фейхоа, я, как зацикленный, ностальгирую всё чаще и больше по этому чуду.  Официально заявляю читающим: даёшь подъем операции Ы! Хуже с ёлкой бог экспериментирует.','2022-05-27','10000000000','Uncomplete',NULL,'/Феникс проекты/купить пиво/Говноед Давид Евревич',4),
 (23,1,2,'купить шарик','Вступив в бой с шипящими змеями — эфой и гадюкой, — маленький, цепкий, храбрый ёж съел их.  Государев указ: душегубцев да шваль всякую высечь, да калёным железом по щекам этих физиономий съездить!  Друг мой эльф! Яшке б свёз птиц южных чащ!  Завершён ежегодный съезд эрудированных школьников, мечтающих глубоко проникнуть в тайны физических явлений и химических реакций.  Здесь фабула объять не может всех эмоций — шепелявый скороход в юбке тащит горячий мёд.  Лингвисты в ужасе: фиг выговоришь этюд: «подъём челябинский, запах щец».  Любя, съешь щипцы, — вздохнёт мэр, — кайф жгуч.  Мюзикл-буфф «Огнедышащий простужается ночью» (в 12345 сценах и 67890 эпизодах).  Обдав его удушающей пылью, множество ярких фаэтонов исчезло из цирка.  Однажды съев фейхоа, я, как зацикленный, ностальгирую всё чаще и больше по этому чуду.  Официально заявляю читающим: даёшь подъем операции Ы! Хуже с ёлкой бог экспериментирует.','2022-05-27','10000000000','Uncomplete',NULL,'/Феникс проекты/купить пиво/Админ',4),
 (24,2,2,'купить шарик','Вступив в бой с шипящими змеями — эфой и гадюкой, — маленький, цепкий, храбрый ёж съел их.  Государев указ: душегубцев да шваль всякую высечь, да калёным железом по щекам этих физиономий съездить!  Друг мой эльф! Яшке б свёз птиц южных чащ!  Завершён ежегодный съезд эрудированных школьников, мечтающих глубоко проникнуть в тайны физических явлений и химических реакций.  Здесь фабула объять не может всех эмоций — шепелявый скороход в юбке тащит горячий мёд.  Лингвисты в ужасе: фиг выговоришь этюд: «подъём челябинский, запах щец».  Любя, съешь щипцы, — вздохнёт мэр, — кайф жгуч.  Мюзикл-буфф «Огнедышащий простужается ночью» (в 12345 сценах и 67890 эпизодах).  Обдав его удушающей пылью, множество ярких фаэтонов исчезло из цирка.  Однажды съев фейхоа, я, как зацикленный, ностальгирую всё чаще и больше по этому чуду.  Официально заявляю читающим: даёшь подъем операции Ы! Хуже с ёлкой бог экспериментирует.','2022-05-27','10000000000','Uncomplete',NULL,'/Феникс проекты/купить пиво/Сергей',4),
 (25,4,2,'купить шарик','Вступив в бой с шипящими змеями — эфой и гадюкой, — маленький, цепкий, храбрый ёж съел их.  Государев указ: душегубцев да шваль всякую высечь, да калёным железом по щекам этих физиономий съездить!  Друг мой эльф! Яшке б свёз птиц южных чащ!  Завершён ежегодный съезд эрудированных школьников, мечтающих глубоко проникнуть в тайны физических явлений и химических реакций.  Здесь фабула объять не может всех эмоций — шепелявый скороход в юбке тащит горячий мёд.  Лингвисты в ужасе: фиг выговоришь этюд: «подъём челябинский, запах щец».  Любя, съешь щипцы, — вздохнёт мэр, — кайф жгуч.  Мюзикл-буфф «Огнедышащий простужается ночью» (в 12345 сценах и 67890 эпизодах).  Обдав его удушающей пылью, множество ярких фаэтонов исчезло из цирка.  Однажды съев фейхоа, я, как зацикленный, ностальгирую всё чаще и больше по этому чуду.  Официально заявляю читающим: даёшь подъем операции Ы! Хуже с ёлкой бог экспериментирует.','2022-05-27','10000000000','Uncomplete',NULL,'/Феникс проекты/купить пиво/Говноед Давид Евревич',4),
 (26,1,2,'купить шарик','Вступив в бой с шипящими змеями — эфой и гадюкой, — маленький, цепкий, храбрый ёж съел их.  Государев указ: душегубцев да шваль всякую высечь, да калёным железом по щекам этих физиономий съездить!  Друг мой эльф! Яшке б свёз птиц южных чащ!  Завершён ежегодный съезд эрудированных школьников, мечтающих глубоко проникнуть в тайны физических явлений и химических реакций.  Здесь фабула объять не может всех эмоций — шепелявый скороход в юбке тащит горячий мёд.  Лингвисты в ужасе: фиг выговоришь этюд: «подъём челябинский, запах щец».  Любя, съешь щипцы, — вздохнёт мэр, — кайф жгуч.  Мюзикл-буфф «Огнедышащий простужается ночью» (в 12345 сценах и 67890 эпизодах).  Обдав его удушающей пылью, множество ярких фаэтонов исчезло из цирка.  Однажды съев фейхоа, я, как зацикленный, ностальгирую всё чаще и больше по этому чуду.  Официально заявляю читающим: даёшь подъем операции Ы! Хуже с ёлкой бог экспериментирует.','2022-05-27','10000000000','Uncomplete',NULL,'/Феникс проекты/купить пиво/Админ',4),
 (27,2,2,'купить шарик','Вступив в бой с шипящими змеями — эфой и гадюкой, — маленький, цепкий, храбрый ёж съел их.  Государев указ: душегубцев да шваль всякую высечь, да калёным железом по щекам этих физиономий съездить!  Друг мой эльф! Яшке б свёз птиц южных чащ!  Завершён ежегодный съезд эрудированных школьников, мечтающих глубоко проникнуть в тайны физических явлений и химических реакций.  Здесь фабула объять не может всех эмоций — шепелявый скороход в юбке тащит горячий мёд.  Лингвисты в ужасе: фиг выговоришь этюд: «подъём челябинский, запах щец».  Любя, съешь щипцы, — вздохнёт мэр, — кайф жгуч.  Мюзикл-буфф «Огнедышащий простужается ночью» (в 12345 сценах и 67890 эпизодах).  Обдав его удушающей пылью, множество ярких фаэтонов исчезло из цирка.  Однажды съев фейхоа, я, как зацикленный, ностальгирую всё чаще и больше по этому чуду.  Официально заявляю читающим: даёшь подъем операции Ы! Хуже с ёлкой бог экспериментирует.','2022-05-27','10000000000','Uncomplete',NULL,'/Феникс проекты/купить пиво/Сергей',4),
 (28,4,2,'купить шарик','Вступив в бой с шипящими змеями — эфой и гадюкой, — маленький, цепкий, храбрый ёж съел их.  Государев указ: душегубцев да шваль всякую высечь, да калёным железом по щекам этих физиономий съездить!  Друг мой эльф! Яшке б свёз птиц южных чащ!  Завершён ежегодный съезд эрудированных школьников, мечтающих глубоко проникнуть в тайны физических явлений и химических реакций.  Здесь фабула объять не может всех эмоций — шепелявый скороход в юбке тащит горячий мёд.  Лингвисты в ужасе: фиг выговоришь этюд: «подъём челябинский, запах щец».  Любя, съешь щипцы, — вздохнёт мэр, — кайф жгуч.  Мюзикл-буфф «Огнедышащий простужается ночью» (в 12345 сценах и 67890 эпизодах).  Обдав его удушающей пылью, множество ярких фаэтонов исчезло из цирка.  Однажды съев фейхоа, я, как зацикленный, ностальгирую всё чаще и больше по этому чуду.  Официально заявляю читающим: даёшь подъем операции Ы! Хуже с ёлкой бог экспериментирует.','2022-05-27','10000000000','Uncomplete',NULL,'/Феникс проекты/купить пиво/Говноед Давид Евревич',4);
COMMIT;
