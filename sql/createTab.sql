-- 建库
create database if not exists Movies;
use Movies;

-- 建表

CREATE TABLE `tb_movie`
(
    `id`        int unsigned    NOT NULL DEFAULT 0 COMMENT '主键ID',
    `title`     varchar(200)    NOT NULL DEFAULT '' COMMENT '电影标题',
    `intros`    varchar(1024)   NOT NULL DEFAULT '' COMMENT '简介',
    `nexturl`   varchar(200)    NOT NULL DEFAULT '' COMMENT '到详情页的url',
    `rate`      decimal(3,1)    NOT NULL DEFAULT 0.0 COMMENT '评分',
    `img`       varchar(200)    NOT NULL DEFAULT '' COMMENT '图片url',
    `summary`   text            NOT NULL COMMENT '电影摘要',
    `deleted`   tinyint         NOT NULL DEFAULT 0 comment '软删标识，0：未删除，1：已删除',
    `ctime`     DATETIME        NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
    `mtime`     DATETIME        NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '修改时间',
    PRIMARY KEY (`id`),
    INDEX       `ix_mtime` (`mtime`)
) ENGINE = InnoDB COMMENT ='电影表';
