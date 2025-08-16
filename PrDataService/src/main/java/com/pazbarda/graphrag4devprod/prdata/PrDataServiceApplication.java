package com.pazbarda.graphrag4devprod.prdata;

import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;

import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

@SpringBootApplication
public class PrDataServiceApplication {
    private static final Logger logger = LoggerFactory.getLogger(PrDataServiceApplication.class);
    public static void main(String[] args) {
        logger.info("Started");
        SpringApplication.run(PrDataServiceApplication.class, args);
        logger.info("running");
    }
}