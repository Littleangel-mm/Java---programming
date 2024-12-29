const mysql = require('mysql2');

const connection = mysql.createConnection({
    host: 'localhost',
    user: 'root',
    password: 'fl3692458121',
    database: 'xtsdb',
    port: 3306,
});

connection.connect((err) => {
    if (err) {
        console.error('数据库连接失败: ' + err.stack);
        return;
    }
    console.log('已连接到数据库');

    connection.query('SELECT * FROM xts_test', (error, results, fields) => {
        if (error) {
            console.error('查询失败: ' + error.stack);
        } else {
            console.log('查询结果:', results);
        }

        connection.end((err) => {
            if (err) {
                console.error('关闭连接失败: ' + err.stack);
            } else {
                console.log('数据库连接已关闭');
            }
        });
    });
});


