const tg = window.Telegram.WebApp;
tg.expand();

const LEVELS = ['A0', 'A1', 'A2', 'B1', 'B2'];

const DB = {
    'A0': [
        {
            id: 'A0_L1',
            title: 'Урок 1: Глагол to be',
            theory: [
                `📘 <b>Глагол TO BE (быть)</b>\n\nЭто самый важный глагол в английском! Он не переводится как "быть", а показывает состояние.\n\n<b>Формы:</b>\n• I <b>am</b> (я есть)\n• He/She/It <b>is</b> (он/она/оно есть)\n• You/We/They <b>are</b> (ты/мы/они есть)\n\nПример: I am a student. (Я студент)`,
                `📝 <b>Отрицания и вопросы</b>\n\n<b>Отрицание:</b> добавляем NOT\n• I am<b>not</b> happy\n• She is<b>not</b> (isn't) here\n• They are<b>not</b> (aren't) ready\n\n<b>Вопрос:</b> меняем местами\n• <b>Are</b> you ready? (Ты готов?)\n• <b>Is</b> she a doctor? (Она врач?)`,
                `💡 <b>Запомни!</b>\n\nГлагол to be используется для:\n1. Описания: She <b>is</b> beautiful\n2. Профессии: I <b>am</b> a teacher\n3. Места: We <b>are</b> at home\n4. Возраста: He <b>is</b> 25\n\nНажми "К тесту", чтобы проверить знания!`
            ],
            questions: [
                { q: 'I ___ a student.', a: ['am', 'is', 'are', 'be'], c: 0 },
                { q: 'She ___ my sister.', a: ['am', 'is', 'are', 'be'], c: 1 },
                { q: 'They ___ at home.', a: ['am', 'is', 'are', 'be'], c: 2 },
                { q: '___ you happy?', a: ['Am', 'Is', 'Are', 'Be'], c: 2 },
                { q: 'He ___ not ready.', a: ['am', 'is', 'are', 'be'], c: 1 },
                { q: 'We ___ friends.', a: ['am', 'is', 'are', 'be'], c: 2 },
                { q: 'It ___ a cat.', a: ['am', 'is', 'are', 'be'], c: 1 },
                { q: '___ she a doctor?', a: ['Am', 'Is', 'Are', 'Be'], c: 1 },
                { q: 'I ___ not tired.', a: ['am', 'is', 'are', 'be'], c: 0 },
                { q: 'You ___ very kind.', a: ['am', 'is', 'are', 'be'], c: 2 },
                { q: 'My name ___ Anna.', a: ['am', 'is', 'are', 'be'], c: 1 },
                { q: '___ they students?', a: ['Am', 'Is', 'Are', 'Be'], c: 2 },
                { q: 'This ___ my book.', a: ['am', 'is', 'are', 'be'], c: 1 },
                { q: 'I ___ 20 years old.', a: ['am', 'is', 'are', 'be'], c: 0 },
                { q: 'She ___ not at work.', a: ['am', 'is', 'are', 'be'], c: 1 },
                { q: '___ I late?', a: ['Am', 'Is', 'Are', 'Be'], c: 0 },
                { q: 'These ___ apples.', a: ['am', 'is', 'are', 'be'], c: 2 },
                { q: 'He ___ my brother.', a: ['am', 'is', 'are', 'be'], c: 1 },
                { q: 'We ___ not hungry.', a: ['am', 'is', 'are', 'be'], c: 2 },
                { q: '___ it cold today?', a: ['Am', 'Is', 'Are', 'Be'], c: 1 }
            ]
        },
        {
            id: 'A0_L2',
            title: 'Урок 2: Местоимения',
            theory: [
                `📘 <b>Личные местоимения</b>\n\nЗаменяют существительные:\n\n<b>Подлежащее:</b>\n• I (я)\n• You (ты, вы)\n• He (он)\n• She (она)\n• It (оно)\n• We (мы)\n• They (они)`,
                `📝 <b>Притяжательные местоимения</b>\n\nПоказывают принадлежность:\n\n• <b>My</b> book (моя книга)\n• <b>Your</b> car (твоя машина)\n• <b>His</b> dog (его собака)\n• <b>Her</b> cat (её кошка)\n• <b>Our</b> house (наш дом)\n• <b>Their</b> friends (их друзья)`,
                `💡 <b>Разница:</b>\n\nI <b>am</b> happy. (Я счастлив)\n<b>My</b> name is... (Моё имя...)\n\nHe <b>is</b> here. (Он здесь)\nThis is <b>his</b> bag. (Это его сумка)\n\nЗапомни: my/your/his/her - ВСЕГДА с существительным!`
            ],
            questions: [
                { q: '___ am a teacher.', a: ['I', 'Me', 'My', 'Mine'], c: 0 },
                { q: 'This is ___ book.', a: ['I', 'me', 'my', 'mine'], c: 2 },
                { q: '___ is my friend.', a: ['He', 'Him', 'His', 'Hers'], c: 0 },
                { q: 'I like ___ car.', a: ['you', 'your', 'yours', 'ours'], c: 1 },
                { q: '___ are students.', a: ['We', 'Us', 'Our', 'Ours'], c: 0 },
                { q: 'That is ___ cat.', a: ['she', 'her', 'hers', 'herself'], c: 1 },
                { q: '___ name is John.', a: ['He', 'Him', 'His', 'Hers'], c: 2 },
                { q: 'They are ___ friends.', a: ['we', 'us', 'our', 'ours'], c: 2 },
                { q: '___ is a doctor.', a: ['She', 'Her', 'Hers', 'Herself'], c: 0 },
                { q: 'I know ___.', a: ['they', 'them', 'their', 'theirs'], c: 1 },
                { q: '___ house is big.', a: ['They', 'Them', 'Their', 'Theirs'], c: 2 },
                { q: 'Can you help ___?', a: ['I', 'me', 'my', 'mine'], c: 1 },
                { q: '___ parents are nice.', a: ['We', 'Us', 'Our', 'Ours'], c: 2 },
                { q: 'This is not ___ bag.', a: ['I', 'me', 'my', 'mine'], c: 2 },
                { q: '___ love music.', a: ['We', 'Us', 'Our', 'Ours'], c: 0 },
                { q: 'Is this ___ pen?', a: ['you', 'your', 'yours', 'ours'], c: 1 },
                { q: '___ brother is tall.', a: ['He', 'Him', 'His', 'Hers'], c: 2 },
                { q: 'I see ___.', a: ['she', 'her', 'hers', 'herself'], c: 1 },
                { q: '___ are happy.', a: ['They', 'Them', 'Their', 'Theirs'], c: 0 },
                { q: 'That is ___ idea.', a: ['we', 'us', 'our', 'ours'], c: 2 }
            ]
        },
        {
            id: 'A0_L3',
            title: 'Урок 3: Артикли',
            theory: [
                `📘 <b>Неопределённый артикль A/AN</b>\n\nИспользуется с исчисляемыми существительными в единственном числе:\n\n• <b>a</b> + согласный: a book, a cat, a dog\n• <b>an</b> + гласный: an apple, an egg, an hour\n\nПереводится как "один/какой-то"`,
                `📝 <b>Определённый артикль THE</b>\n\nИспользуется когда:\n1. Предмет уже упоминался\n2. Предмет единственный (the sun, the moon)\n3. Конкретный предмет\n\nПример: I have a book. <b>The</b> book is interesting.`,
                `💡 <b>Когда НЕ нужен артикль:</b>\n\n• Имена: Anna (не the Anna)\n• Множественное число (вообще): Cats are cute\n• Абстрактные понятия: Love is beautiful\n\nЗапомни: a/an = один из многих, the = конкретный`
            ],
            questions: [
                { q: 'I have ___ apple.', a: ['a', 'an', 'the', '-'], c: 1 },
                { q: 'She is ___ doctor.', a: ['a', 'an', 'the', '-'], c: 0 },
                { q: '___ sun is hot.', a: ['A', 'An', 'The', '-'], c: 2 },
                { q: 'This is ___ book.', a: ['a', 'an', 'the', '-'], c: 0 },
                { q: 'I see ___ elephant.', a: ['a', 'an', 'the', '-'], c: 1 },
                { q: '___ moon is beautiful.', a: ['A', 'An', 'The', '-'], c: 2 },
                { q: 'He has ___ car.', a: ['a', 'an', 'the', '-'], c: 0 },
                { q: '___ Earth is round.', a: ['A', 'An', 'The', '-'], c: 2 },
                { q: 'It is ___ umbrella.', a: ['a', 'an', 'the', '-'], c: 1 },
                { q: 'I want ___ coffee.', a: ['a', 'an', 'the', '-'], c: 3 },
                { q: '___ cat is on the table.', a: ['A', 'An', 'The', '-'], c: 2 },
                { q: 'She has ___ idea.', a: ['a', 'an', 'the', '-'], c: 1 },
                { q: '___ water is cold.', a: ['A', 'An', 'The', '-'], c: 3 },
                { q: 'This is ___ egg.', a: ['a', 'an', 'the', '-'], c: 1 },
                { q: '___ dog is barking.', a: ['A', 'An', 'The', '-'], c: 2 },
                { q: 'He is ___ honest man.', a: ['a', 'an', 'the', '-'], c: 1 },
                { q: 'I need ___ pen.', a: ['a', 'an', 'the', '-'], c: 0 },
                { q: '___ sky is blue.', a: ['A', 'An', 'The', '-'], c: 2 },
                { q: 'She eats ___ banana.', a: ['a', 'an', 'the', '-'], c: 0 },
                { q: '___ music is loud.', a: ['A', 'An', 'The', '-'], c: 3 }
            ]
        },
        {
            id: 'A0_L4',
            title: 'Урок 4: Вопросительные слова',
            theory: [
                `📘 <b>Основные вопросительные слова</b>\n\n• <b>What</b> - что, какой\n• <b>Where</b> - где, куда\n• <b>Who</b> - кто\n• <b>When</b> - когда\n• <b>Why</b> - почему`,
                `📝 <b>How и How much/many</b>\n\n• <b>How</b> - как\n• <b>How much</b> - сколько (неисчисляемое)\n• <b>How many</b> - сколько (исчисляемое)\n\nПримеры:\nHow are you? (Как дела?)\nHow much water? (Сколько воды?)\nHow many books? (Сколько книг?)`,
                `💡 <b>Структура вопроса:</b>\n\nВопросительное слово + вспомогательный глагол + подлежащее\n\n<b>What</b> do you like?\n<b>Where</b> is she?\n<b>When</b> are they coming?\n<b>Why</b> is he sad?`
            ],
            questions: [
                { q: '___ is your name?', a: ['What', 'Where', 'Who', 'When'], c: 0 },
                { q: '___ do you live?', a: ['What', 'Where', 'Who', 'When'], c: 1 },
                { q: '___ is she?', a: ['What', 'Where', 'Who', 'When'], c: 2 },
                { q: '___ is your birthday?', a: ['What', 'Where', 'Who', 'When'], c: 3 },
                { q: '___ are you sad?', a: ['What', 'Where', 'Why', 'When'], c: 2 },
                { q: '___ are you?', a: ['What', 'How', 'Why', 'When'], c: 1 },
                { q: '___ much is it?', a: ['What', 'How', 'Why', 'When'], c: 1 },
                { q: '___ many friends?', a: ['What', 'How', 'Why', 'When'], c: 1 },
                { q: '___ color do you like?', a: ['What', 'Where', 'Who', 'When'], c: 0 },
                { q: '___ is the station?', a: ['What', 'Where', 'Who', 'When'], c: 1 },
                { q: '___ is your teacher?', a: ['What', 'Where', 'Who', 'When'], c: 2 },
                { q: '___ do you work?', a: ['What', 'Where', 'When', 'Why'], c: 2 },
                { q: '___ don\'t you like it?', a: ['What', 'Where', 'Why', 'When'], c: 2 },
                { q: '___ old are you?', a: ['What', 'How', 'Why', 'When'], c: 1 },
                { q: '___ time is it?', a: ['What', 'Where', 'Who', 'When'], c: 0 },
                { q: '___ is your bag?', a: ['What', 'Where', 'Who', 'When'], c: 1 },
                { q: '___ is that man?', a: ['What', 'Where', 'Who', 'When'], c: 2 },
                { q: '___ do you study?', a: ['What', 'Where', 'When', 'Why'], c: 2 },
                { q: '___ is the problem?', a: ['What', 'Where', 'Who', 'When'], c: 0 },
                { q: '___ are you late?', a: ['What', 'Where', 'Why', 'When'], c: 2 }
            ]
        }
    ],
    'A1': [
        {
            id: 'A1_L1',
            title: 'Урок 1: Present Simple',
            theory: [
                `📘 <b>Present Simple (Настоящее простое)</b>\n\nИспользуется для:\n1. Регулярных действий\n2. Фактов\n3. Расписаний\n\nФорма: I/You/We/They + глагол\nHe/She/It + глагол + <b>s</b>`,
                `📝 <b>Окончание -s/-es</b>\n\nДобавляем к глаголу для he/she/it:\n\n• Большинство: work<b>s</b>, play<b>s</b>\n• После s/sh/ch/x/o: go<b>es</b>, watch<b>es</b>\n• После согласной + y: stud<b>ies</b> (y→ies)\n\nОтрицание: don't/doesn't + глагол`,
                `💡 <b>Маркеры времени:</b>\n\n• always (всегда)\n• usually (обычно)\n• often (часто)\n• sometimes (иногда)\n• never (никогда)\n• every day (каждый день)\n\nI <b>always</b> drink coffee. She <b>never</b> eats meat.`
            ],
            questions: [
                { q: 'I ___ coffee every day.', a: ['drink', 'drinks', 'drinking', 'drank'], c: 0 },
                { q: 'She ___ to music.', a: ['listen', 'listens', 'listening', 'listened'], c: 1 },
                { q: 'They ___ football on Sundays.', a: ['play', 'plays', 'playing', 'played'], c: 0 },
                { q: 'He ___ up at 7 am.', a: ['get', 'gets', 'getting', 'got'], c: 1 },
                { q: 'We ___ English.', a: ['study', 'studies', 'studying', 'studied'], c: 0 },
                { q: 'My cat ___ milk.', a: ['like', 'likes', 'liking', 'liked'], c: 1 },
                { q: 'I ___ not like tea.', a: ['do', 'does', 'doing', 'did'], c: 0 },
                { q: 'She ___ not work here.', a: ['do', 'does', 'doing', 'did'], c: 1 },
                { q: '___ you speak English?', a: ['Do', 'Does', 'Doing', 'Did'], c: 0 },
                { q: '___ he know you?', a: ['Do', 'Does', 'Doing', 'Did'], c: 1 },
                { q: 'The sun ___ in the east.', a: ['rise', 'rises', 'rising', 'rose'], c: 1 },
                { q: 'Water ___ at 100°C.', a: ['boil', 'boils', 'boiling', 'boiled'], c: 1 },
                { q: 'She ___ TV every evening.', a: ['watch', 'watches', 'watching', 'watched'], c: 1 },
                { q: 'They ___ to school by bus.', a: ['go', 'goes', 'going', 'went'], c: 0 },
                { q: 'He ___ his homework.', a: ['do', 'does', 'doing', 'did'], c: 1 },
                { q: 'I ___ pizza.', a: ['love', 'loves', 'loving', 'loved'], c: 0 },
                { q: 'My sister ___ in London.', a: ['live', 'lives', 'living', 'lived'], c: 1 },
                { q: 'We ___ early.', a: ['wake', 'wakes', 'waking', 'woke'], c: 0 },
                { q: 'The train ___ at 9.', a: ['leave', 'leaves', 'leaving', 'left'], c: 1 },
                { q: '___ she play tennis?', a: ['Do', 'Does', 'Doing', 'Did'], c: 1 }
            ]
        },
        {
            id: 'A1_L2',
            title: 'Урок 2: Present Continuous',
            theory: [
                `📘 <b>Present Continuous (Настоящее длительное)</b>\n\nДействие происходит СЕЙЧАС:\n\nФорма: am/is/are + глагол + <b>ing</b>\n\n• I <b>am working</b>\n• He/She/It <b>is working</b>\n• You/We/They <b>are working</b>`,
                `📝 <b>Правила добавления -ing</b>\n\n1. Просто + ing: work<b>ing</b>, play<b>ing</b>\n2. Немая e → ing: mak<b>ing</b>, tak<b>ing</b>\n3. Краткая гласная + согласная → удваиваем: sit<b>ting</b>, run<b>ning</b>\n\nОтрицание: am/is/are + NOT + ing`,
                `💡 <b>Present Simple vs Continuous</b>\n\nSimple: факт, регулярность\nI <b>work</b> every day.\n\nContinuous: сейчас, в момент речи\nI <b>am working</b> now.\n\nМаркеры Continuous: now, at the moment, today, Look!`
            ],
            questions: [
                { q: 'I ___ now.', a: ['work', 'am working', 'works', 'working'], c: 1 },
                { q: 'She ___ TV at the moment.', a: ['watch', 'is watching', 'watches', 'watching'], c: 1 },
                { q: 'They ___ football now.', a: ['play', 'are playing', 'plays', 'playing'], c: 1 },
                { q: 'He ___ right now.', a: ['sleep', 'is sleeping', 'sleeps', 'sleeping'], c: 1 },
                { q: 'We ___ dinner.', a: ['cook', 'are cooking', 'cooks', 'cooking'], c: 1 },
                { q: 'It ___ outside.', a: ['rain', 'is raining', 'rains', 'raining'], c: 1 },
                { q: 'I ___ not sleeping.', a: ['am', 'is', 'are', 'be'], c: 0 },
                { q: 'She ___ not working today.', a: ['am', 'is', 'are', 'be'], c: 1 },
                { q: '___ you listening?', a: ['Am', 'Is', 'Are', 'Be'], c: 2 },
                { q: '___ he coming?', a: ['Am', 'Is', 'Are', 'Be'], c: 1 },
                { q: 'Look! It ___.', a: ['snow', 'is snowing', 'snows', 'snowed'], c: 1 },
                { q: 'I ___ for the bus.', a: ['wait', 'am waiting', 'waits', 'waited'], c: 1 },
                { q: 'They ___ to music.', a: ['listen', 'are listening', 'listens', 'listened'], c: 1 },
                { q: 'She ___ a book now.', a: ['read', 'is reading', 'reads', 'reading'], c: 1 },
                { q: 'We ___ home.', a: ['go', 'are going', 'goes', 'went'], c: 1 },
                { q: 'He ___ his car.', a: ['wash', 'is washing', 'washes', 'washed'], c: 1 },
                { q: 'The children ___.', a: ['play', 'are playing', 'plays', 'played'], c: 1 },
                { q: 'I ___ coffee.', a: ['drink', 'am drinking', 'drinks', 'drank'], c: 1 },
                { q: 'She ___ to work.', a: ['drive', 'is driving', 'drives', 'drove'], c: 1 },
                { q: 'They ___ lunch.', a: ['have', 'are having', 'has', 'had'], c: 1 }
            ]
        },
        {
            id: 'A1_L3',
            title: 'Урок 3: Past Simple',
            theory: [
                `📘 <b>Past Simple (Прошедшее простое)</b>\n\nДействие завершилось в прошлом:\n\nПравильные глаголы: глагол + <b>ed</b>\nwork → work<b>ed</b>\nplay → play<b>ed</b>\n\nНеправильные: нужно учить (таблица)`,
                `📝 <b>Неправильные глаголы</b>\n\n• go → <b>went</b>\n• see → <b>saw</b>\n• eat → <b>ate</b>\n• have → <b>had</b>\n• do → <b>did</b>\n• come → <b>came</b>\n• take → <b>took</b>\n• make → <b>made</b>\n\nОтрицание: didn't + глагол (без ed!)`,
                `💡 <b>Маркеры Past Simple:</b>\n\n• yesterday (вчера)\n• last week/month/year\n• ...ago (2 days ago)\n• in 2010\n\nI <b>went</b> to Paris <b>last year</b>.\nShe <b>didn't call</b> me <b>yesterday</b>.`
            ],
            questions: [
                { q: 'I ___ to the cinema yesterday.', a: ['go', 'went', 'gone', 'going'], c: 1 },
                { q: 'She ___ a book last week.', a: ['read', 'read', 'reading', 'reads'], c: 0 },
                { q: 'They ___ pizza for dinner.', a: ['eat', 'ate', 'eaten', 'eating'], c: 1 },
                { q: 'He ___ his homework.', a: ['do', 'did', 'done', 'doing'], c: 1 },
                { q: 'We ___ TV last night.', a: ['watch', 'watched', 'watching', 'watches'], c: 1 },
                { q: 'I ___ not see him.', a: ['do', 'did', 'done', 'doing'], c: 1 },
                { q: 'She ___ come to the party.', a: ['do', 'did', 'done', 'doing'], c: 1 },
                { q: '___ you like the film?', a: ['Do', 'Did', 'Done', 'Doing'], c: 1 },
                { q: '___ he call you?', a: ['Do', 'Did', 'Done', 'Doing'], c: 1 },
                { q: 'I ___ a car in 2020.', a: ['buy', 'bought', 'buyed', 'buying'], c: 1 },
                { q: 'She ___ to London last year.', a: ['fly', 'flew', 'flown', 'flying'], c: 1 },
                { q: 'They ___ the game.', a: ['win', 'won', 'winned', 'winning'], c: 1 },
                { q: 'He ___ me a letter.', a: ['write', 'wrote', 'written', 'writing'], c: 1 },
                { q: 'We ___ the bus.', a: ['miss', 'missed', 'missing', 'misses'], c: 1 },
                { q: 'I ___ tired yesterday.', a: ['be', 'was', 'were', 'been'], c: 1 },
                { q: 'She ___ happy.', a: ['be', 'was', 'were', 'been'], c: 1 },
                { q: 'They ___ at home.', a: ['be', 'was', 'were', 'been'], c: 2 },
                { q: 'I ___ breakfast at 8.', a: ['have', 'had', 'has', 'having'], c: 1 },
                { q: 'He ___ his keys.', a: ['lose', 'lost', 'losed', 'losing'], c: 1 },
                { q: 'We ___ a great time.', a: ['have', 'had', 'has', 'having'], c: 1 }
            ]
        },
        {
            id: 'A1_L4',
            title: 'Урок 4: Предлоги',
            theory: [
                `📘 <b>Предлоги времени IN/ON/AT</b>\n\n<b>AT</b> - точное время:\nat 5 o'clock, at noon, at night\n\n<b>ON</b> - дни и даты:\non Monday, on my birthday, on May 1st\n\n<b>IN</b> - месяцы, годы, части дня:\nin July, in 2020, in the morning`,
                `📝 <b>Предлоги места</b>\n\n<b>AT</b> - точка:\nat home, at work, at the station\n\n<b>ON</b> - поверхность:\non the table, on the wall, on the floor\n\n<b>IN</b> - внутри:\nin the room, in the box, in London`,
                `💡 <b>Запомни:</b>\n\nIN the morning/afternoon/evening\nBUT AT night\n\nON the weekend (амер.)\nAT the weekend (брит.)\n\nIN a car, ON a bus/train/plane`
            ],
            questions: [
                { q: 'I work ___ Monday.', a: ['in', 'on', 'at', 'to'], c: 1 },
                { q: 'She was born ___ 1995.', a: ['in', 'on', 'at', 'to'], c: 0 },
                { q: 'We meet ___ 5 pm.', a: ['in', 'on', 'at', 'to'], c: 2 },
                { q: 'The book is ___ the table.', a: ['in', 'on', 'at', 'to'], c: 1 },
                { q: 'He lives ___ London.', a: ['in', 'on', 'at', 'to'], c: 0 },
                { q: 'I sleep ___ night.', a: ['in', 'on', 'at', 'to'], c: 2 },
                { q: 'She works ___ the office.', a: ['in', 'on', 'at', 'to'], c: 2 },
                { q: 'We go skiing ___ winter.', a: ['in', 'on', 'at', 'to'], c: 0 },
                { q: 'My birthday is ___ May.', a: ['in', 'on', 'at', 'to'], c: 0 },
                { q: 'The picture is ___ the wall.', a: ['in', 'on', 'at', 'to'], c: 1 },
                { q: 'I get up ___ 7 o\'clock.', a: ['in', 'on', 'at', 'to'], c: 2 },
                { q: 'They arrived ___ the airport.', a: ['in', 'on', 'at', 'to'], c: 2 },
                { q: 'She is ___ home now.', a: ['in', 'on', 'at', 'to'], c: 2 },
                { q: 'We met ___ a party.', a: ['in', 'on', 'at', 'to'], c: 2 },
                { q: 'The keys are ___ my bag.', a: ['in', 'on', 'at', 'to'], c: 0 },
                { q: 'I read ___ the evening.', a: ['in', 'on', 'at', 'to'], c: 0 },
                { q: 'He was born ___ June 5th.', a: ['in', 'on', 'at', 'to'], c: 1 },
                { q: 'We travel ___ summer.', a: ['in', 'on', 'at', 'to'], c: 0 },
                { q: 'The cat is ___ the chair.', a: ['in', 'on', 'at', 'to'], c: 1 },
                { q: 'I\'ll see you ___ Friday.', a: ['in', 'on', 'at', 'to'], c: 1 }
            ]
        }
    ],
    'A2': [
        {
            id: 'A2_L1',
            title: 'Урок 1: Present Perfect',
            theory: [
                `📘 <b>Present Perfect (Настоящее совершённое)</b>\n\nСвязь прошлого с настоящим:\n\nФорма: have/has + <b>V3</b> (3 форма)\n\nI/You/We/They <b>have worked</b>\nHe/She/It <b>has worked</b>\n\nПравильные: V3 = ed\nНеправильные: таблица`,
                `📝 <b>Когда используем?</b>\n\n1. Результат сейчас:\nI <b>have lost</b> my keys. (и сейчас нет)\n\n2. Опыт жизни:\nI <b>have been</b> to Paris.\n\n3. Недавнее действие:\nShe <b>has just arrived</b>.`,
                `💡 <b>Маркеры:</b>\n\n• already (уже)\n• yet (ещё нет/уже?)\n• just (только что)\n• ever (когда-либо)\n• never (никогда)\n• for (в течение)\n• since (с)\n\nI <b>have already done</b> it.`
            ],
            questions: [
                { q: 'I ___ my homework.', a: ['finish', 'have finished', 'has finished', 'finished'], c: 1 },
                { q: 'She ___ to Paris.', a: ['be', 'have been', 'has been', 'was'], c: 2 },
                { q: 'They ___ the film.', a: ['see', 'have seen', 'has seen', 'saw'], c: 1 },
                { q: 'He ___ his keys.', a: ['lose', 'have lost', 'has lost', 'lost'], c: 2 },
                { q: 'We ___ here for 2 years.', a: ['live', 'have lived', 'has lived', 'lived'], c: 1 },
                { q: 'I ___ not seen him.', a: ['have', 'has', 'had', 'having'], c: 0 },
                { q: 'She ___ not called yet.', a: ['have', 'has', 'had', 'having'], c: 1 },
                { q: '___ you ever been to Spain?', a: ['Have', 'Has', 'Had', 'Having'], c: 0 },
                { q: '___ he finished work?', a: ['Have', 'Has', 'Had', 'Having'], c: 1 },
                { q: 'I have ___ eaten sushi.', a: ['never', 'ever', 'yet', 'since'], c: 0 },
                { q: 'She has ___ arrived.', a: ['just', 'yet', 'since', 'for'], c: 0 },
                { q: 'Have you done it ___?', a: ['already', 'yet', 'since', 'for'], c: 1 },
                { q: 'I have ___ met her.', a: ['already', 'yet', 'since', 'for'], c: 0 },
                { q: 'We have known him ___ 2010.', a: ['since', 'for', 'yet', 'already'], c: 0 },
                { q: 'They have lived here ___ 5 years.', a: ['since', 'for', 'yet', 'already'], c: 1 },
                { q: 'He has ___ called me.', a: ['never', 'ever', 'yet', 'since'], c: 0 },
                { q: 'Have you ___ tried sushi?', a: ['never', 'ever', 'yet', 'since'], c: 1 },
                { q: 'I have ___ finished.', a: ['just', 'yet', 'since', 'for'], c: 0 },
                { q: 'She has worked here ___ 2015.', a: ['since', 'for', 'yet', 'already'], c: 0 },
                { q: 'We have ___ been to Japan.', a: ['never', 'ever', 'yet', 'since'], c: 0 }
            ]
        },
        {
            id: 'A2_L2',
            title: 'Урок 2: Future Simple',
            theory: [
                `📘 <b>Future Simple (Будущее простое)</b>\n\nСпонтанные решения, предсказания:\n\nФорма: <b>will</b> + глагол\n\nI/You/He/She/It/We/They <b>will work</b>\n\nСокращение: I'll, you'll, he'll...`,
                `📝 <b>Когда используем?</b>\n\n1. Спонтанное решение:\nI <b>'ll help</b> you!\n\n2. Предсказание:\nIt <b>will rain</b> tomorrow.\n\n3. Обещание:\nI <b>will call</b> you.\n\nОтрицание: will not (won't) + глагол`,
                `💡 <b>Will vs Going to</b>\n\n<b>Will</b> - решение в момент речи:\nI'll have coffee.\n\n<b>Going to</b> - план заранее:\nI'm going to buy a car.\n\nВопрос: Will you...?\nОтвет: Yes, I will. / No, I won't.`
            ],
            questions: [
                { q: 'I ___ help you.', a: ['will', 'am', 'do', 'have'], c: 0 },
                { q: 'She ___ call you later.', a: ['will', 'am', 'do', 'have'], c: 0 },
                { q: 'They ___ come tomorrow.', a: ['will', 'are', 'do', 'have'], c: 0 },
                { q: 'It ___ rain today.', a: ['will', 'is', 'does', 'has'], c: 0 },
                { q: 'We ___ be late.', a: ['will', 'are', 'do', 'have'], c: 0 },
                { q: 'I ___ not go.', a: ['will', 'am', 'do', 'have'], c: 0 },
                { q: 'He ___ not tell anyone.', a: ['will', 'is', 'does', 'has'], c: 0 },
                { q: '___ you help me?', a: ['Will', 'Are', 'Do', 'Have'], c: 0 },
                { q: '___ she come?', a: ['Will', 'Is', 'Does', 'Has'], c: 0 },
                { q: 'I think it ___ be sunny.', a: ['will', 'is', 'does', 'has'], c: 0 },
                { q: 'Maybe I ___ stay home.', a: ['will', 'am', 'do', 'have'], c: 0 },
                { q: 'She ___ probably arrive late.', a: ['will', 'is', 'does', 'has'], c: 0 },
                { q: 'I promise I ___ call.', a: ['will', 'am', 'do', 'have'], c: 0 },
                { q: 'They ___ never know.', a: ['will', 'are', 'do', 'have'], c: 0 },
                { q: 'He ___ be 30 next year.', a: ['will', 'is', 'does', 'has'], c: 0 },
                { q: 'We ___ miss you.', a: ['will', 'are', 'do', 'have'], c: 0 },
                { q: 'I ___ always love you.', a: ['will', 'am', 'do', 'have'], c: 0 },
                { q: '___ they agree?', a: ['Will', 'Are', 'Do', 'Have'], c: 0 },
                { q: 'I ___ do it now.', a: ['will', 'am', 'do', 'have'], c: 0 },
                { q: 'She ___ not like it.', a: ['will', 'is', 'does', 'has'], c: 0 }
            ]
        },
        {
            id: 'A2_L3',
            title: 'Урок 3: Модальные глаголы',
            theory: [
                `📘 <b>Can/Could (мочь, уметь)</b>\n\n<b>Can</b> - способность сейчас:\nI <b>can</b> swim.\n\n<b>Could</b> - способность в прошлом:\nI <b>could</b> run fast when I was young.\n\nВопрос: Can you help me?`,
                `📝 <b>Must/Have to (должен)</b>\n\n<b>Must</b> - личная обязанность:\nI <b>must</b> study.\n\n<b>Have to</b> - внешнее правило:\nI <b>have to</b> wear a uniform.\n\n<b>Mustn't</b> - запрещено:\nYou <b>mustn't</b> smoke here.`,
                `💡 <b>Should (следует)</b>\n\nСовет, рекомендация:\n\nYou <b>should</b> see a doctor.\nYou <b>shouldn't</b> eat so much.\n\nЗапомни: после модальных глаголов ВСЕГДА инфинитив без to (кроме have to)`
            ],
            questions: [
                { q: 'I ___ swim.', a: ['can', 'must', 'should', 'have'], c: 0 },
                { q: '___ you help me?', a: ['Can', 'Must', 'Should', 'Have'], c: 0 },
                { q: 'She ___ speak French.', a: ['can', 'must', 'should', 'have'], c: 0 },
                { q: 'I ___ go now.', a: ['must', 'can', 'should', 'have'], c: 0 },
                { q: 'You ___ smoke here.', a: ['mustn\'t', 'can\'t', 'shouldn\'t', 'haven\'t'], c: 0 },
                { q: 'We ___ wear a helmet.', a: ['have to', 'can', 'should', 'must'], c: 0 },
                { q: 'He ___ work tomorrow.', a: ['has to', 'can', 'should', 'must'], c: 0 },
                { q: 'You ___ see a doctor.', a: ['should', 'can', 'must', 'have'], c: 0 },
                { q: 'I ___ not find my keys.', a: ['can', 'must', 'should', 'have'], c: 0 },
                { q: 'She ___ not come.', a: ['can', 'must', 'should', 'have'], c: 0 },
                { q: '___ I open the window?', a: ['Can', 'Must', 'Should', 'Have'], c: 0 },
                { q: 'You ___ eat more vegetables.', a: ['should', 'can', 'must', 'have'], c: 0 },
                { q: 'They ___ not park here.', a: ['mustn\'t', 'can\'t', 'shouldn\'t', 'haven\'t'], c: 0 },
                { q: 'I ___ run fast when I was young.', a: ['could', 'can', 'must', 'should'], c: 0 },
                { q: 'We ___ leave now.', a: ['must', 'can', 'should', 'have'], c: 0 },
                { q: 'You ___ try this restaurant.', a: ['should', 'can', 'must', 'have'], c: 0 },
                { q: 'He ___ not drive.', a: ['can\'t', 'mustn\'t', 'shouldn\'t', 'haven\'t'], c: 0 },
                { q: '___ we go?', a: ['Can', 'Must', 'Should', 'Have'], c: 0 },
                { q: 'I ___ finish this today.', a: ['must', 'can', 'should', 'have'], c: 0 },
                { q: 'You ___ be more careful.', a: ['should', 'can', 'must', 'have'], c: 0 }
            ]
        },
        {
            id: 'A2_L4',
            title: 'Урок 4: Степени сравнения',
            theory: [
                `📘 <b>Сравнительная степень</b>\n\nСравнение двух предметов:\n\nКороткие: прил + <b>er</b> + than\ntall → tall<b>er than</b>\n\nДлинные: <b>more</b> + прил + than\nbeautiful → <b>more</b> beautiful <b>than</b>\n\nИсключения: good → better, bad → worse`,
                `📝 <b>Превосходная степень</b>\n\nЛучший из многих:\n\nКороткие: <b>the</b> + прил + <b>est</b>\ntall → <b>the tall<b>est</b></b>\n\nДлинные: <b>the most</b> + прил\nbeautiful → <b>the most</b> beautiful\n\nИсключения: good → the best, bad → the worst`,
                `💡 <b>Правила:</b>\n\n1. Краткая гласная + согласная → удваиваем: big → bigger\n2. Согласная + y → ier: happy → happier\n3. Двусложные на -y: happier, easier\n4. Остальные двусложные и более: more/most`
            ],
            questions: [
                { q: 'She is ___ than me.', a: ['tall', 'taller', 'tallest', 'more tall'], c: 1 },
                { q: 'This is ___ book.', a: ['good', 'better', 'best', 'the best'], c: 3 },
                { q: 'He is ___ student.', a: ['intelligent', 'more intelligent', 'most intelligent', 'the most intelligent'], c: 3 },
                { q: 'My car is ___ than yours.', a: ['fast', 'faster', 'fastest', 'more fast'], c: 1 },
                { q: 'This is ___ day of my life!', a: ['happy', 'happier', 'happiest', 'the happiest'], c: 3 },
                { q: 'She is ___ than her sister.', a: ['beautiful', 'more beautiful', 'most beautiful', 'the most beautiful'], c: 1 },
                { q: 'I am ___ than you.', a: ['old', 'older', 'oldest', 'more old'], c: 1 },
                { q: 'This is ___ film I\'ve seen.', a: ['bad', 'worse', 'worst', 'the worst'], c: 3 },
                { q: 'He runs ___ than me.', a: ['fast', 'faster', 'fastest', 'more fast'], c: 1 },
                { q: 'She is ___ person I know.', a: ['kind', 'kinder', 'kindest', 'the kindest'], c: 3 },
                { q: 'This box is ___ than that one.', a: ['heavy', 'heavier', 'heaviest', 'more heavy'], c: 1 },
                { q: 'It\'s ___ today than yesterday.', a: ['cold', 'colder', 'coldest', 'more cold'], c: 1 },
                { q: 'He is ___ boy in the class.', a: ['tall', 'taller', 'tallest', 'the tallest'], c: 3 },
                { q: 'This is ___ restaurant.', a: ['expensive', 'more expensive', 'most expensive', 'the most expensive'], c: 3 },
                { q: 'She feels ___ than before.', a: ['good', 'better', 'best', 'the best'], c: 1 },
                { q: 'This is ___ question.', a: ['easy', 'easier', 'easiest', 'the easiest'], c: 3 },
                { q: 'He is ___ than his brother.', a: ['strong', 'stronger', 'strongest', 'more strong'], c: 1 },
                { q: 'It\'s ___ way.', a: ['short', 'shorter', 'shortest', 'the shortest'], c: 3 },
                { q: 'She is ___ than me.', a: ['happy', 'happier', 'happiest', 'more happy'], c: 1 },
                { q: 'This is ___ book.', a: ['interesting', 'more interesting', 'most interesting', 'the most interesting'], c: 3 }
            ]
        }
    ],
    'B1': [
        {
            id: 'B1_L1',
            title: 'Урок 1: Conditionals (0 и 1)',
            theory: [
                `📘 <b>Zero Conditional</b>\n\nФакты, законы природы:\n\n<b>If</b> + Present Simple, Present Simple\n\n<b>If you heat</b> water, <b>it boils</b>.\n<b>If it rains</b>, <b>I take</b> an umbrella.\n\nЭто всегда правда!`,
                `📝 <b>First Conditional</b>\n\nРеальная ситуация в будущем:\n\n<b>If</b> + Present Simple, <b>will</b> + глагол\n\n<b>If it rains</b>, <b>I will stay</b> home.\n<b>If you study</b>, <b>you will pass</b>.\n\nВозможно случится!`,
                `💡 <b>Разница:</b>\n\n<b>Zero</b> - всегда правда (факт)\nIf you freeze water, it becomes ice.\n\n<b>First</b> - возможно в будущем\nIf it rains tomorrow, I'll cancel the trip.\n\nМожно использовать: unless (если не), when (когда)`
            ],
            questions: [
                { q: 'If you ___ water, it boils.', a: ['heat', 'will heat', 'heated', 'heating'], c: 0 },
                { q: 'If it rains, I ___ an umbrella.', a: ['take', 'will take', 'took', 'taking'], c: 0 },
                { q: 'If you ___ hard, you will succeed.', a: ['work', 'will work', 'worked', 'working'], c: 0 },
                { q: 'If she ___ late, we will start without her.', a: ['is', 'will be', 'was', 'being'], c: 0 },
                { q: 'Plants die if they ___ water.', a: ['don\'t get', 'won\'t get', 'didn\'t get', 'not get'], c: 0 },
                { q: 'If you ___ me, I will help you.', a: ['ask', 'will ask', 'asked', 'asking'], c: 0 },
                { q: 'If he ___ the bus, he will be late.', a: ['misses', 'will miss', 'missed', 'missing'], c: 0 },
                { q: 'I will call you if I ___ time.', a: ['have', 'will have', 'had', 'having'], c: 0 },
                { q: 'If you ___ sugar in tea, it dissolves.', a: ['put', 'will put', 'putted', 'putting'], c: 0 },
                { q: 'She will be angry if you ___ late.', a: ['are', 'will be', 'were', 'being'], c: 0 },
                { q: 'If it ___ sunny, we will go to the beach.', a: ['is', 'will be', 'was', 'being'], c: 0 },
                { q: 'You will get tired if you ___ too much.', a: ['work', 'will work', 'worked', 'working'], c: 0 },
                { q: 'If I ___ enough money, I will buy a car.', a: ['have', 'will have', 'had', 'having'], c: 0 },
                { q: 'Ice melts if you ___ it.', a: ['heat', 'will heat', 'heated', 'heating'], c: 0 },
                { q: 'If they ___ the train, they will miss the meeting.', a: ['miss', 'will miss', 'missed', 'missing'], c: 0 },
                { q: 'He will pass if he ___.', a: ['studies', 'will study', 'studied', 'studying'], c: 0 },
                { q: 'If you ___ spicy food, you drink water.', a: ['eat', 'will eat', 'ate', 'eating'], c: 0 },
                { q: 'I will be happy if you ___.', a: ['come', 'will come', 'came', 'coming'], c: 0 },
                { q: 'If she ___ hard, she will win.', a: ['tries', 'will try', 'tried', 'trying'], c: 0 },
                { q: 'You will learn if you ___.', a: ['practice', 'will practice', 'practiced', 'practicing'], c: 0 }
            ]
        },
        {
            id: 'B1_L2',
            title: 'Урок 2: Past Continuous',
            theory: [
                `📘 <b>Past Continuous (Прошедшее длительное)</b>\n\nДействие длилось в конкретный момент прошлого:\n\nwas/were + глагол + <b>ing</b>\n\nI <b>was working</b> at 5 pm yesterday.\nThey <b>were playing</b> when I arrived.`,
                `📝 <b>Past Simple vs Continuous</b>\n\n<b>Continuous</b> - длительное действие:\nI <b>was reading</b> when you called.\n\n<b>Simple</b> - короткое, прерывающее:\nI <b>read</b> a book yesterday.\n\nWhen + Simple, Continuous\nWhile + Continuous, Simple/Continuous`,
                `💡 <b>Примеры:</b>\n\nI <b>was sleeping</b> when the phone <b>rang</b>.\nWhile I <b>was cooking</b>, she <b>was watching</b> TV.\n\nWhat <b>were</b> you <b>doing</b> at 8 pm?\nI <b>was having</b> dinner.`
            ],
            questions: [
                { q: 'I ___ at 8 pm yesterday.', a: ['worked', 'was working', 'work', 'am working'], c: 1 },
                { q: 'She ___ when I called.', a: ['slept', 'was sleeping', 'sleeps', 'is sleeping'], c: 1 },
                { q: 'They ___ football at 3 pm.', a: ['played', 'were playing', 'play', 'are playing'], c: 1 },
                { q: 'What ___ you doing?', a: ['did', 'were', 'do', 'are'], c: 1 },
                { q: 'He ___ TV when I arrived.', a: ['watched', 'was watching', 'watches', 'is watching'], c: 1 },
                { q: 'We ___ dinner at 7 pm.', a: ['had', 'were having', 'have', 'are having'], c: 1 },
                { q: 'I ___ not sleeping.', a: ['did', 'was', 'do', 'am'], c: 1 },
                { q: 'They ___ not working.', a: ['did', 'were', 'do', 'are'], c: 1 },
                { q: '___ you watching TV?', a: ['Did', 'Were', 'Do', 'Are'], c: 1 },
                { q: '___ she studying?', a: ['Did', 'Was', 'Does', 'Is'], c: 1 },
                { q: 'While I ___, it started to rain.', a: ['walked', 'was walking', 'walk', 'am walking'], c: 1 },
                { q: 'He ___ when the phone rang.', a: ['cooked', 'was cooking', 'cooks', 'is cooking'], c: 1 },
                { q: 'We ___ to music all evening.', a: ['listened', 'were listening', 'listen', 'are listening'], c: 1 },
                { q: 'What ___ she doing at 9?', a: ['did', 'was', 'does', 'is'], c: 1 },
                { q: 'I ___ for you all day.', a: ['waited', 'was waiting', 'wait', 'am waiting'], c: 1 },
                { q: 'They ___ when we came.', a: ['argued', 'were arguing', 'argue', 'are arguing'], c: 1 },
                { q: 'She ___ a book while he was watching TV.', a: ['read', 'was reading', 'reads', 'is reading'], c: 1 },
                { q: 'I ___ about you yesterday.', a: ['thought', 'was thinking', 'think', 'am thinking'], c: 1 },
                { q: 'The sun ___ when we left.', a: ['shone', 'was shining', 'shines', 'is shining'], c: 1 },
                { q: 'We ___ not expecting you.', a: ['did', 'were', 'do', 'are'], c: 1 }
            ]
        },
        {
            id: 'B1_L3',
            title: 'Урок 3: Reported Speech',
            theory: [
                `📘 <b>Косвенная речь</b>\n\nПередаём чужие слова:\n\nПрямая: "I am happy", he said.\nКосвенная: He said (that) he <b>was</b> happy.\n\nВремя сдвигается назад!`,
                `📝 <b>Сдвиг времён</b>\n\nPresent → Past\n"I like it" → He said he <b>liked</b> it.\n\nPresent Perfect → Past Perfect\n"I have done it" → He said he <b>had done</b> it.\n\nPast → Past Perfect (или остаётся Past)\n"I did it" → He said he <b>had done</b> it.`,
                `💡 <b>Изменения:</b>\n\nМестоимения: I → he/she, we → they\n\nВремя: now → then, today → that day, \nyesterday → the day before, tomorrow → the next day\n\nHe said, "I will call you tomorrow."\n→ He said he would call me the next day.`
            ],
            questions: [
                { q: 'He said he ___ tired.', a: ['is', 'was', 'were', 'been'], c: 1 },
                { q: 'She said she ___ English.', a: ['like', 'liked', 'likes', 'liking'], c: 1 },
                { q: 'They said they ___ busy.', a: ['are', 'were', 'was', 'been'], c: 1 },
                { q: 'He said he ___ the film.', a: ['like', 'liked', 'likes', 'liking'], c: 1 },
                { q: 'She said she ___ to Paris.', a: ['go', 'went', 'gone', 'going'], c: 1 },
                { q: 'He said he ___ me.', a: ['help', 'helped', 'would help', 'helping'], c: 2 },
                { q: 'She said she ___ call.', a: ['will', 'would', 'can', 'could'], c: 1 },
                { q: 'They said they ___ coming.', a: ['are', 'were', 'was', 'been'], c: 1 },
                { q: 'He said it ___ raining.', a: ['is', 'was', 'were', 'been'], c: 1 },
                { q: 'She said she ___ hungry.', a: ['is', 'was', 'were', 'been'], c: 1 },
                { q: 'He said he ___ finished.', a: ['has', 'had', 'have', 'having'], c: 1 },
                { q: 'She said she ___ seen it.', a: ['has', 'had', 'have', 'having'], c: 1 },
                { q: 'They said they ___ there before.', a: ['have been', 'had been', 'has been', 'were'], c: 1 },
                { q: 'He said he ___ work.', a: ['must', 'had to', 'has to', 'having to'], c: 1 },
                { q: 'She said she ___ swim.', a: ['can', 'could', 'will', 'would'], c: 1 },
                { q: 'He said, "I ___ busy."', a: ['am', 'was', 'were', 'been'], c: 0 },
                { q: 'She said, "I ___ it tomorrow."', a: ['do', 'will do', 'would do', 'did'], c: 1 },
                { q: 'He said, "I ___ you."', a: ['help', 'will help', 'would help', 'helped'], c: 1 },
                { q: 'She said, "I ___ late."', a: ['am', 'will be', 'would be', 'was'], c: 1 },
                { q: 'He said he ___ agree.', a: ['don\'t', 'didn\'t', 'won\'t', 'wouldn\'t'], c: 1 }
            ]
        },
        {
            id: 'B1_L4',
            title: 'Урок 4: Пассивный залог',
            theory: [
                `📘 <b>Passive Voice (Пассив)</b>\n\nПодлежащее - объект действия:\n\nActive: Someone <b>made</b> this table.\nPassive: This table <b>was made</b> (by someone).\n\nbe + V3 (3 форма глагола)`,
                `📝 <b>Формы Passive</b>\n\nPresent: is/are + V3\nThe letter <b>is written</b>.\n\nPast: was/were + V3\nThe letter <b>was written</b>.\n\nPresent Perfect: have/has been + V3\nThe letter <b>has been written</b>.`,
                `💡 <b>Когда используем?</b>\n\n1. Неважно кто сделал:\nEnglish <b>is spoken</b> here.\n\n2. Очевидно кто:\nThe thief <b>was arrested</b>.\n\n3. Формальный стиль:\nYou <b>are required</b> to sign.\n\nby + агент (если важно кто)`
            ],
            questions: [
                { q: 'English ___ here.', a: ['speak', 'is spoken', 'spoke', 'spoken'], c: 1 },
                { q: 'The book ___ in 2020.', a: ['publish', 'published', 'was published', 'publishing'], c: 2 },
                { q: 'The room ___ every day.', a: ['clean', 'cleans', 'is cleaned', 'cleaned'], c: 2 },
                { q: 'The car ___ yesterday.', a: ['repair', 'repaired', 'was repaired', 'repairing'], c: 2 },
                { q: 'Letters ___ by post.', a: ['send', 'sends', 'are sent', 'sent'], c: 2 },
                { q: 'The window ___ last week.', a: ['break', 'broke', 'was broken', 'broken'], c: 2 },
                { q: 'Coffee ___ in Brazil.', a: ['grow', 'grows', 'is grown', 'grown'], c: 2 },
                { q: 'The decision ___ already.', a: ['make', 'made', 'has been made', 'making'], c: 2 },
                { q: 'The house ___ in 1990.', a: ['build', 'built', 'was built', 'building'], c: 2 },
                { q: 'Milk ___ in the fridge.', a: ['keep', 'keeps', 'is kept', 'kept'], c: 2 },
                { q: 'The game ___ at 8 pm.', a: ['play', 'plays', 'is played', 'played'], c: 2 },
                { q: 'The letter ___ tomorrow.', a: ['send', 'sends', 'will be sent', 'sent'], c: 2 },
                { q: 'Photos ___ by tourists.', a: ['take', 'takes', 'are taken', 'taken'], c: 2 },
                { q: 'The problem ___ now.', a: ['solve', 'solves', 'is being solved', 'solved'], c: 2 },
                { q: 'Rice ___ in Asia.', a: ['grow', 'grows', 'is grown', 'grown'], c: 2 },
                { q: 'The meeting ___ cancelled.', a: ['be', 'been', 'was', 'is'], c: 2 },
                { q: 'The work ___ finished.', a: ['has', 'have', 'has been', 'have been'], c: 2 },
                { q: 'Cars ___ in this factory.', a: ['make', 'makes', 'are made', 'made'], c: 2 },
                { q: 'The food ___ delicious.', a: ['smell', 'smells', 'is smelt', 'smelled'], c: 2 },
                { q: 'The news ___ yesterday.', a: ['announce', 'announced', 'was announced', 'announcing'], c: 2 }
            ]
        }
    ],
    'B2': [
        {
            id: 'B2_L1',
            title: 'Урок 1: Second Conditional',
            theory: [
                `📘 <b>Second Conditional</b>\n\nНереальная ситуация сейчас/вообще:\n\n<b>If</b> + Past Simple, <b>would</b> + глагол\n\n<b>If I had</b> money, <b>I would buy</b> a car.\n(но денег нет)\n\n<b>If I were</b> you, <b>I would go</b>.\n(совет, но я не ты)`,
                `📝 <b>Когда используем?</b>\n\n1. Маловероятно:\nIf I won the lottery, I would travel.\n\n2. Невозможно:\nIf I were rich, I would help everyone.\n\n3. Совет:\nIf I were you, I would apologize.\n\nWere вместо was для всех лиц (формально)`,
                `💡 <b>Примеры:</b>\n\nIf I <b>had</b> more time, I <b>would learn</b> Japanese.\n(но времени нет)\n\nIf she <b>knew</b>, she <b>would tell</b> us.\n(но она не знает)\n\nWhat <b>would</b> you do if you <b>met</b> an alien?`
            ],
            questions: [
                { q: 'If I ___ rich, I would buy a house.', a: ['am', 'was', 'were', 'been'], c: 2 },
                { q: 'If she ___ time, she would help.', a: ['has', 'had', 'have', 'having'], c: 1 },
                { q: 'I would travel if I ___ money.', a: ['have', 'had', 'has', 'having'], c: 1 },
                { q: 'If I ___ you, I would go.', a: ['am', 'was', 'were', 'been'], c: 2 },
                { q: 'He would call if he ___.', a: ['knows', 'knew', 'know', 'known'], c: 1 },
                { q: 'If they ___, they would come.', a: ['can', 'could', 'will', 'would'], c: 1 },
                { q: 'I would help if I ___.', a: ['can', 'could', 'will', 'would'], c: 1 },
                { q: 'If she ___, she would be happy.', a: ['knows', 'knew', 'know', 'known'], c: 1 },
                { q: 'We would go if it ___ sunny.', a: ['is', 'was', 'were', 'been'], c: 1 },
                { q: 'If I ___ a bird, I would fly.', a: ['am', 'was', 'were', 'been'], c: 2 },
                { q: 'He would pass if he ___.', a: ['studies', 'studied', 'study', 'studying'], c: 1 },
                { q: 'If they ___ faster, they would win.', a: ['run', 'ran', 'runned', 'running'], c: 1 },
                { q: 'I would tell you if I ___.', a: ['know', 'knew', 'known', 'knowing'], c: 1 },
                { q: 'If she ___, she would succeed.', a: ['tries', 'tried', 'try', 'trying'], c: 1 },
                { q: 'We would stay if we ___.', a: ['can', 'could', 'will', 'would'], c: 1 },
                { q: 'If I ___ the answer, I would tell you.', a: ['know', 'knew', 'known', 'knowing'], c: 1 },
                { q: 'He would be happier if he ___.', a: ['works', 'worked', 'work', 'working'], c: 1 },
                { q: 'If they ___ us, they would come.', a: ['invite', 'invited', 'invites', 'inviting'], c: 1 },
                { q: 'I would do it if I ___ how.', a: ['know', 'knew', 'known', 'knowing'], c: 1 },
                { q: 'If she ___, she would understand.', a: ['listens', 'listened', 'listen', 'listening'], c: 1 }
            ]
        },
        {
            id: 'B2_L2',
            title: 'Урок 2: Third Conditional',
            theory: [
                `📘 <b>Third Conditional</b>\n\nНереальная ситуация в ПРОШЛОМ:\n\n<b>If</b> + Past Perfect, <b>would have</b> + V3\n\n<b>If I had studied</b>, <b>I would have passed</b>.\n(но я не учился и не сдал)\n\nЭто сожаление о прошлом!`,
                `📝 <b>Когда используем?</b>\n\n1. Сожаление:\nIf I had known, I would have helped.\n(но я не знал)\n\n2. Критика:\nIf you had listened, you wouldn't have made mistakes.\n\n3. Воображение прошлого:\nIf she had taken the job, she would have moved to London.`,
                `💡 <b>Примеры:</b>\n\nIf I <b>had seen</b> him, I <b>would have said</b> hello.\n(но я не видел)\n\nIf they <b>had left</b> earlier, they <b>wouldn't have missed</b> the train.\n\nWhat <b>would</b> you <b>have done</b> if you <b>had been</b> there?`
            ],
            questions: [
                { q: 'If I had known, I ___ you.', a: ['would help', 'would have helped', 'will help', 'helped'], c: 1 },
                { q: 'If she ___, she would have come.', a: ['knew', 'had known', 'knows', 'knowing'], c: 1 },
                { q: 'I would have called if I ___ time.', a: ['had', 'had had', 'have', 'having'], c: 1 },
                { q: 'If they ___, they would have won.', a: ['practiced', 'had practiced', 'practice', 'practicing'], c: 1 },
                { q: 'He would have passed if he ___.', a: ['studied', 'had studied', 'studies', 'studying'], c: 1 },
                { q: 'If I ___ you, I would have gone.', a: ['was', 'were', 'had been', 'have been'], c: 2 },
                { q: 'She would have been happy if you ___.', a: ['came', 'had come', 'come', 'coming'], c: 1 },
                { q: 'If we ___, we wouldn\'t have been late.', a: ['left', 'had left', 'leave', 'leaving'], c: 1 },
                { q: 'I would have helped if you ___ me.', a: ['asked', 'had asked', 'ask', 'asking'], c: 1 },
                { q: 'If it ___, we would have gone out.', a: ['didn\'t rain', 'hadn\'t rained', 'doesn\'t rain', 'not raining'], c: 1 },
                { q: 'He would have seen it if he ___.', a: ['looked', 'had looked', 'looks', 'looking'], c: 1 },
                { q: 'If they ___, they would have succeeded.', a: ['tried', 'had tried', 'try', 'trying'], c: 1 },
                { q: 'I would have bought it if it ___ cheaper.', a: ['was', 'were', 'had been', 'has been'], c: 2 },
                { q: 'If she ___, she would have understood.', a: ['listened', 'had listened', 'listens', 'listening'], c: 1 },
                { q: 'We would have stayed if we ___.', a: ['knew', 'had known', 'know', 'knowing'], c: 1 },
                { q: 'If I ___, I would have told you.', a: ['saw', 'had seen', 'see', 'seeing'], c: 1 },
                { q: 'He would have been angry if he ___.', a: ['knew', 'had known', 'knows', 'knowing'], c: 1 },
                { q: 'If they ___, they would have arrived on time.', a: ['left', 'had left', 'leave', 'leaving'], c: 1 },
                { q: 'I would have come if I ___ sick.', a: ['wasn\'t', 'hadn\'t been', 'am not', 'not being'], c: 1 },
                { q: 'If she ___, she would have passed.', a: ['studied', 'had studied', 'studies', 'studying'], c: 1 }
            ]
        },
        {
            id: 'B2_L3',
            title: 'Урок 3: Mixed Conditionals',
            theory: [
                `📘 <b>Mixed Conditionals</b>\n\nСмешиваем времена для сложных ситуаций:\n\nПрошлое → Сейчас:\nIf + Past Perfect, would + глагол\n\nIf I <b>had studied</b> medicine, I <b>would be</b> a doctor now.\n(учился в прошлом → был бы сейчас)`,
                `📝 <b>Сейчас → Прошлое:</b>\n\nIf + Past Simple, would have + V3\n\nIf I <b>were</b> smarter, I <b>would have solved</b> the problem.\n(вообще не умный → не решил тогда)\n\nIf she <b>spoke</b> English, she <b>would have got</b> the job.`,
                `💡 <b>Примеры:</b>\n\nIf I <b>had taken</b> that job, I <b>would be</b> rich now.\n(взял бы тогда → был бы сейчас)\n\nIf he <b>were</b> more careful, he <b>wouldn't have crashed</b> the car.\n(вообще неосторожный → разбил тогда)`
            ],
            questions: [
                { q: 'If I had studied, I ___ a doctor now.', a: ['would be', 'would have been', 'will be', 'was'], c: 0 },
                { q: 'If she were smarter, she ___ the test.', a: ['would pass', 'would have passed', 'will pass', 'passed'], c: 1 },
                { q: 'If I had saved money, I ___ rich now.', a: ['would be', 'would have been', 'will be', 'was'], c: 0 },
                { q: 'If he were taller, he ___ basketball.', a: ['would play', 'would have played', 'will play', 'played'], c: 0 },
                { q: 'If they had left earlier, they ___ here now.', a: ['would be', 'would have been', 'will be', 'were'], c: 0 },
                { q: 'If I spoke French, I ___ that job.', a: ['would get', 'would have got', 'will get', 'got'], c: 1 },
                { q: 'If she had married him, she ___ happy now.', a: ['would be', 'would have been', 'will be', 'was'], c: 0 },
                { q: 'If I were you, I ___ that mistake.', a: ['wouldn\'t make', 'wouldn\'t have made', 'won\'t make', 'didn\'t make'], c: 1 },
                { q: 'If he had practiced, he ___ better now.', a: ['would play', 'would have played', 'will play', 'played'], c: 0 },
                { q: 'If they were richer, they ___ that house.', a: ['would buy', 'would have bought', 'will buy', 'bought'], c: 1 },
                { q: 'If I had known, I ___ here now.', a: ['would be', 'would have been', 'will be', 'was'], c: 0 },
                { q: 'If she were more careful, she ___ her phone.', a: ['wouldn\'t lose', 'wouldn\'t have lost', 'won\'t lose', 'didn\'t lose'], c: 1 },
                { q: 'If he had studied harder, he ___ at university now.', a: ['would be', 'would have been', 'will be', 'was'], c: 0 },
                { q: 'If I were braver, I ___ her.', a: ['would ask', 'would have asked', 'will ask', 'asked'], c: 1 },
                { q: 'If they had invested, they ___ millionaires now.', a: ['would be', 'would have been', 'will be', 'were'], c: 0 },
                { q: 'If she knew the truth, she ___ angry.', a: ['would be', 'would have been', 'will be', 'was'], c: 0 },
                { q: 'If I had taken the job, I ___ in London now.', a: ['would live', 'would have lived', 'will live', 'lived'], c: 0 },
                { q: 'If he were more organized, he ___ late.', a: ['wouldn\'t be', 'wouldn\'t have been', 'won\'t be', 'wasn\'t'], c: 1 },
                { q: 'If they had trained, they ___ the match.', a: ['would win', 'would have won', 'will win', 'won'], c: 1 },
                { q: 'If I were younger, I ___ travel.', a: ['would', 'would have', 'will', 'did'], c: 0 }
            ]
        },
        {
            id: 'B2_L4',
            title: 'Урок 4: Фразовые глаголы',
            theory: [
                `📘 <b>Что такое phrasal verbs?</b>\n\nГлагол + частица = новое значение:\n\nlook (смотреть) + up (вверх) = <b>look up</b> (искать)\ngive (давать) + up (вверх) = <b>give up</b> (сдаваться)\n\nНужно учить как отдельные слова!`,
                `📝 <b>Частые фразовые глаголы:</b>\n\n• <b>get up</b> - вставать\n• <b>look for</b> - искать\n• <b>give up</b> - сдаваться\n• <b>turn on/off</b> - включать/выключать\n• <b>put on</b> - надевать\n• <b>take off</b> - снимать/взлетать\n• <b>come back</b> - возвращаться\n• <b>go on</b> - продолжать`,
                `💡 <b>Примеры:</b>\n\nI <b>get up</b> at 7 am.\nCan you <b>turn on</b> the light?\nDon't <b>give up</b>! Keep trying!\nI'm <b>looking for</b> my keys.\nShe <b>put on</b> her coat and left.\nThe plane <b>takes off</b> at 9.`
            ],
            questions: [
                { q: 'I ___ at 7 am every day.', a: ['get up', 'get on', 'get off', 'get back'], c: 0 },
                { q: 'Can you ___ the light?', a: ['turn on', 'turn off', 'turn up', 'turn down'], c: 0 },
                { q: 'I\'m ___ my keys.', a: ['looking for', 'looking at', 'looking after', 'looking up'], c: 0 },
                { q: 'Don\'t ___! Keep trying!', a: ['give up', 'give in', 'give out', 'give away'], c: 0 },
                { q: 'She ___ her coat.', a: ['put on', 'put off', 'put out', 'put away'], c: 0 },
                { q: 'The plane ___ at 9.', a: ['takes off', 'takes on', 'takes up', 'takes after'], c: 0 },
                { q: 'I\'ll ___ tomorrow.', a: ['come back', 'come on', 'come in', 'come out'], c: 0 },
                { q: 'Please ___ the music.', a: ['turn down', 'turn up', 'turn on', 'turn off'], c: 0 },
                { q: 'He ___ his father.', a: ['takes after', 'takes on', 'takes up', 'takes off'], c: 0 },
                { q: '___ the bus at the next stop.', a: ['Get off', 'Get on', 'Get up', 'Get back'], c: 0 },
                { q: 'I need to ___ early tomorrow.', a: ['get up', 'get on', 'get off', 'get back'], c: 0 },
                { q: 'She ___ the invitation.', a: ['turned down', 'turned up', 'turned on', 'turned off'], c: 0 },
                { q: 'Who will ___ the children?', a: ['look after', 'look for', 'look at', 'look up'], c: 0 },
                { q: 'I ___ an old friend yesterday.', a: ['ran into', 'ran out', 'ran over', 'ran away'], c: 0 },
                { q: 'We ___ milk.', a: ['ran out of', 'ran into', 'ran over', 'ran away'], c: 0 },
                { q: 'Please ___ your shoes.', a: ['take off', 'take on', 'take up', 'take after'], c: 0 },
                { q: 'The meeting was ___ until Monday.', a: ['put off', 'put on', 'put out', 'put away'], c: 0 },
                { q: 'He ___ smoking last year.', a: ['gave up', 'gave in', 'gave out', 'gave away'], c: 0 },
                { q: 'I ___ this word in the dictionary.', a: ['looked up', 'looked for', 'looked after', 'looked at'], c: 0 },
                { q: '___! You can do it!', a: ['Come on', 'Come in', 'Come back', 'Come out'], c: 0 }
            ]
        }
    ]
};

let state = {
    points: 0,
    currentLevel: 'A0',
    isPremium: false,
    lessons: {}
};

function loadState() {
    const saved = localStorage.getItem('aevi_progress');
    if (saved) state = JSON.parse(saved);
}

function saveState() {
    localStorage.setItem('aevi_progress', JSON.stringify(state));
    updateUI();
}

function updateUI() {
    document.getElementById('points-display').textContent = state.points;
    document.getElementById('premium-btn').style.display = state.isPremium ? 'none' : 'block';
    renderLevels();
    renderLessons();
}

function renderLevels() {
    const container = document.getElementById('levels-container');
    container.innerHTML = '';
    LEVELS.forEach(l => {
        if (l === 'B2' && !state.isPremium) return;
        const btn = document.createElement('button');
        btn.className = `level-chip ${state.currentLevel === l ? 'active' : ''}`;
        btn.textContent = l;
        btn.onclick = () => {
            state.currentLevel = l;
            saveState();
        };
        container.appendChild(btn);
    });
}

function renderLessons() {
    const container = document.getElementById('lessons-container');
    container.innerHTML = '';
    const lessons = DB[state.currentLevel] || [];
    lessons.forEach((lesson) => {
        const prog = state.lessons[lesson.id] || { completed: false, theoryViewed: false, score: 0 };
        const card = document.createElement('div');
        card.className = `lesson-card ${prog.completed ? 'completed' : ''}`;
        card.innerHTML = `
            <div class="theory-icon" onclick="event.stopPropagation(); openTheory('${lesson.id}')">?</div>
            <div class="title">${lesson.title}</div>
            <div class="status">${prog.completed ? '✅ Пройден' : (prog.theoryViewed ? '▶️ Доступен' : '📚 Теория')}</div>
        `;
        card.onclick = () => startLesson(lesson.id);
        container.appendChild(card);
    });
}

function showScreen(id) {
    document.querySelectorAll('.screen').forEach(s => s.classList.remove('active'));
    document.getElementById(id).classList.add('active');
}

function goHome() {
    showScreen('home-screen');
    updateUI();
}

document.getElementById('premium-btn').onclick = () => {
    state.isPremium = true;
    tg.showPopup({ title: '🎉 Premium!', message: 'Подписка активирована! Уровень B2 разблокирован.', buttons: [{ type: 'ok' }] });
    saveState();
};

let currentTheoryLessonId = null;
let theoryStep = 0;

function openTheory(lessonId) {
    currentTheoryLessonId = lessonId;
    const lesson = findLesson(lessonId);
    document.getElementById('theory-title').textContent = lesson.title;
    theoryStep = 0;
    renderTheoryStep();
    showScreen('theory-screen');
}

function renderTheoryStep() {
    const lesson = findLesson(currentTheoryLessonId);
    document.getElementById('theory-content').innerHTML = lesson.theory[theoryStep].replace(/\n/g, '<br>');
    document.getElementById('theory-next-btn').textContent = theoryStep < lesson.theory.length - 1 ? 'Далее →' : 'К тесту 🚀';
}

document.getElementById('theory-next-btn').onclick = () => {
    const lesson = findLesson(currentTheoryLessonId);
    if (theoryStep < lesson.theory.length - 1) {
        theoryStep++;
        renderTheoryStep();
    } else {
        if (!state.lessons[lesson.id]) state.lessons[lesson.id] = { completed: false, theoryViewed: false, score: 0 };
        state.lessons[lesson.id].theoryViewed = true;
        saveState();
        startQuiz(lesson.id);
    }
};

let currentQuizLessonId = null;
let quizIndex = 0;
let quizScore = 0;

function startLesson(lessonId) {
    const prog = state.lessons[lessonId];
    if (!prog || !prog.theoryViewed) openTheory(lessonId);
    else startQuiz(lessonId);
}

function startQuiz(lessonId) {
    currentQuizLessonId = lessonId;
    quizIndex = 0; quizScore = 0;
    showScreen('quiz-screen');
    loadQuestion();
}

function findLesson(id) {
    for (const l of LEVELS) {
        const found = DB[l]?.find(x => x.id === id);
        if (found) return found;
    }
    return null;
}

function loadQuestion() {
    const lesson = findLesson(currentQuizLessonId);
    const q = lesson.questions[quizIndex];
    document.getElementById('quiz-step').textContent = quizIndex + 1;
    document.getElementById('quiz-fill').style.width = `${((quizIndex + 1) / lesson.questions.length) * 100}%`;
    document.getElementById('quiz-question').textContent = q.q;
    const opts = document.getElementById('quiz-options');
    opts.innerHTML = '';
    q.a.forEach((ans, i) => {
        const btn = document.createElement('button');
        btn.className = 'option-btn';
        btn.textContent = ans;
        btn.onclick = () => handleAnswer(i, q.c, btn, lesson.questions.length);
        opts.appendChild(btn);
    });
}

function handleAnswer(selected, correct, btn, total) {
    document.querySelectorAll('.option-btn').forEach(b => b.disabled = true);
    if (selected === correct) {
        btn.classList.add('correct'); quizScore++;
        tg.HapticFeedback?.notificationOccurred('success');
    } else {
        btn.classList.add('wrong');
        document.querySelectorAll('.option-btn')[correct].classList.add('correct');
        tg.HapticFeedback?.notificationOccurred('error');
    }
    setTimeout(() => {
        quizIndex++;
        if (quizIndex < total) loadQuestion();
        else finishQuiz();
    }, 800);
}

function finishQuiz() {
    const lesson = findLesson(currentQuizLessonId);
    const pointsEarned = quizScore * 10;
    state.points += pointsEarned;
    state.lessons[lesson.id] = { completed: true, theoryViewed: true, score: quizScore };
    saveState();
    document.getElementById('result-correct').textContent = quizScore;
    document.getElementById('result-points').textContent = pointsEarned;
    showScreen('result-screen');
}

// === ЗАПУСК ===
loadState();
updateUI();

setTimeout(() => {
    const splash = document.getElementById('splash-screen');
    splash.classList.remove('show');
    splash.style.display = 'none';
    showScreen('home-screen');
}, 5000);
