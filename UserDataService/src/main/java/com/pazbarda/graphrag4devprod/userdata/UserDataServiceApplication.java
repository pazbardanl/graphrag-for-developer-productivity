package com.pazbarda.graphrag4devprod.userdata;

import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;

import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

@SpringBootApplication
public class UserDataServiceApplication {
    private static final Logger logger = LoggerFactory.getLogger(UserDataServiceApplication.class);
    public static void main(String[] args) {
        logger.info("Started");
        SpringApplication.run(UserDataServiceApplication.class, args);
        logger.info("running");
    }
}