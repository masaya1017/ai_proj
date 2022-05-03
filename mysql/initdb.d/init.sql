
CREATE TABLE `personal_info` (
    mail_address VARCHAR(100) NOT NULL,
    sex VARCHAR(6) NOT NULL,
    age INT NOT NULL,
    name VARCHAR(50) NOT NULL,
    prefecture VARCHAR(50) NOT NULL,
    createdAt DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updatedAt DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    PRIMARY KEY (mail_address)
);

INSERT INTO `personal_info` (mail_address, sex, age, name, prefecture, createdAt, updatedAt)
VALUES
('hoge1_1@gmail.com', 'male',   18, 'ichirou1' , 'tokyo', current_timestamp(), current_timestamp()),
('hoge2@gmail.com', 'male',   23, 'zirou2', 'osaka', current_timestamp(), current_timestamp()),
('hoge3_3@gmail.com', 'male',   31, 'saburou', 'tokyo', current_timestamp(), current_timestamp()),
('hoge4@gmail.com', 'female', 29, 'itiko', 'tokyo', current_timestamp(), current_timestamp()),
('hoge5_5@gmail.com', 'mail',   11, 'shirou', 'osaka', current_timestamp(), current_timestamp()),
('hoge6@gmail.com', 'female', 42, 'fumiko', 'tokyo', current_timestamp(), current_timestamp());