
CREATE TABLE global_tb
(
    id int PRIMARY KEY GENERATED ALWAYS AS IDENTITY,
    gl_teleg_id varchar(32) NOT NULL,
    gl_role varchar(8) DEFAULT NULL,
    sub_newslet bool DEFAULT False NOT NULL
); 

CREATE TABLE lesson_tb
(
    id int PRIMARY KEY GENERATED ALWAYS AS IDENTITY,
    lesson_name varchar(128) NOT NULL
);

CREATE TABLE group_tb
(
    id int PRIMARY KEY GENERATED ALWAYS AS IDENTITY,
    group_name varchar(32) NOT NULL,
    group_approved bool DEFAULT False NOT NULL
);

CREATE TABLE prepod_tb
(
    id int PRIMARY KEY GENERATED ALWAYS AS IDENTITY,
    prepod_name varchar(64) NOT NULL,
    prepod_approved bool DEFAULT False NOT NULL,
    gl_id int REFERENCES global_tb(id)
);

CREATE TABLE student_tb
(
    id int PRIMARY KEY GENERATED ALWAYS AS IDENTITY,
    student_name varchar(64) NOT NULL,
    gl_id int REFERENCES global_tb(id),
    group_id int REFERENCES group_tb(id)
);

CREATE TABLE connect_tb
(
    id int PRIMARY KEY GENERATED ALWAYS AS IDENTITY,
    group_id int REFERENCES group_tb(id),
    prepod_id int REFERENCES prepod_tb(id),
    lesson_id int REFERENCES lesson_tb(id),
    teach_role varchar(8)
);

CREATE TABLE  question_tb(
    id int PRIMARY KEY GENERATED ALWAYS AS IDENTITY,
    question_name varchar(128)
);

CREATE TABLE groupquestion_tb(
    q_id int REFERENCES question_tb(id) NOT NULL,
    gp_question_id int NOT NULL
);

CREATE TABLE survay_tb(
    id int PRIMARY KEY GENERATED ALWAYS AS IDENTITY,
    survay_code int DEFAULT NULL,
    survay_name varchar(128),
    from_id varchar(32),
    to_group varchar(32),
    groupquestion_id int
);

drop table connect_tb;
drop table teach_tb;
drop table lesson_tb;
drop table student_tb;
drop table group_tb;
drop table global_tb;

drop table survay_tb;
drop table groupquestion_tb;
drop table question_tb;