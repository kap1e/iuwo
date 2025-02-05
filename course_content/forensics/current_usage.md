<h1>Современная форензика</h1>
<p>
    Современная форензика — это ключевой инструмент в борьбе с цифровыми преступлениями, охватывающий множество направлений, включая восстановление данных, анализ сетевого трафика, облачные технологии и мобильные устройства. Основная цель цифровой форензики — сбор, анализ и представление цифровых доказательств в суде, при этом данные должны быть аутентичными, непротиворечивыми и юридически допустимыми.
</p>
<h2>1. Новые вызовы и инструменты</h2>
<p>
    С ростом объёмов данных и разнообразия устройств (от смартфонов до умных датчиков IoT) специалисты по форензике сталкиваются с рядом новых вызовов. Например, шифрование данных, использование анонимных сетей, таких как Tor, и атаки с использованием сложных вредоносных программ требуют применения инновационных подходов. Сегодня эксперты используют передовые инструменты, такие как Autopsy для анализа файловой системы, Wireshark для сетевого мониторинга и анализа трафика, а также облачные платформы, например Magnet Axiom, для обработки данных из социальных сетей или облачных хранилищ.
</p>
<h2>2. Узкоспециализированные направления</h2>
<p>
    Современная форензика охватывает ряд узких направлений. Например, мобильная форензика позволяет извлекать и анализировать данные с телефонов, включая зашифрованные приложения, такие как WhatsApp. Облачная форензика фокусируется на сборе данных из облачных хранилищ и онлайн-сервисов, что особенно актуально в условиях удалённой работы. Ещё одно важное направление — форензика вредоносного ПО, где исследуются механизмы заражения систем и извлекаются артефакты, указывающие на источник атаки.
</p>

<h1>Гайд по Wireshark для CTF</h1>
<p>
    Wireshark — это мощный инструмент для анализа сетевого трафика, который часто используется в CTF-соревнованиях для решения задач, связанных с сетевой форензикой. Этот гайд поможет вам понять основы работы с Wireshark и освоить базовые техники анализа сетевых пакетов.
</p>

<h2>1. Установка и запуск Wireshark</h2>
<p>
    Wireshark можно скачать с официального сайта <a href="https://www.wireshark.org" target="_blank">Wireshark.org</a>. После установки выполните следующие шаги:
</p>
<ul>
    <li>Запустите Wireshark и выберите сетевой интерфейс, который вы хотите прослушивать (например, Ethernet или Wi-Fi).</li>
    <li>Нажмите кнопку «Start» для начала захвата пакетов.</li>
</ul>

<h2>2. Основные функции и фильтры</h2>
<p>
    Wireshark предлагает множество фильтров, которые помогают сузить поиск и найти нужные данные. Вот несколько полезных фильтров:
</p>
<ul>
    <li><strong>http:</strong> для отображения HTTP-трафика.</li>
    <li><strong>ip.src == 192.168.1.1:</strong> фильтрует пакеты, отправленные с указанного IP-адреса.</li>
    <li><strong>dns:</strong> отображает только DNS-запросы.</li>
</ul>
<p>
    Для анализа данных достаточно выбрать нужный пакет и перейти в нижнюю часть окна, где содержится информация о пакетах в виде сырого текста и интерпретированных данных.
</p>

<h2>3. Решение типичного CTF-задания</h2>
<p>
    Пример: вам предоставлен файл с захваченным трафиком (PCAP). Ваша задача — найти текстовый флаг, который передавался по HTTP:
</p>
<ol>
    <li>Откройте файл PCAP в Wireshark.</li>
    <li>Используйте фильтр <strong>http</strong> для отображения только HTTP-трафика.</li>
    <li>Найдите пакеты с полезной нагрузкой (например, GET или POST-запросы).</li>
    <li>Кликните на нужный пакет и изучите данные в разделе "Follow TCP Stream".</li>
    <li>В извлечённом содержимом найдите флаг, например, <code>CTF{Wireshark_Analysis_Success}</code>.</li>
</ol>

<h2>4. Дополнительные советы</h2>
<p>
    Если задача сложнее и данные скрыты в зашифрованном или бинарном виде, используйте дополнительные инструменты, такие как CyberChef, для декодирования содержимого. Также не забывайте про встроенные функции Wireshark для декодирования файлов, например, извлечения объектов из HTTP-трафика.
</p>
