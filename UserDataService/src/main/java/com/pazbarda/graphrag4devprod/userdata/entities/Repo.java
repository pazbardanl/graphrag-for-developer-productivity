package com.pazbarda.graphrag4devprod.userdata.entities;

import jakarta.persistence.Entity;
import jakarta.persistence.GeneratedValue;
import jakarta.persistence.GenerationType;
import jakarta.persistence.Id;
import jakarta.persistence.Table;

@Entity
@Table(name = "repos")
public class Repo {
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Integer id;
    private String name;
    private String reviewerSelectorStrategy;

    public Integer getId() {
        return id;
    }
    public void setId(Integer id) {
        this.id = id;
    }
    public String getName() {
        return name;
    }
    public void setName(String name) {
        this.name = name;
    }
    public String getReviewerSelectorStrategy() {
        return reviewerSelectorStrategy;
    }
    public void setReviewerSelectorStrategy(String reviewerSelectorStrategy) {
        this.reviewerSelectorStrategy = reviewerSelectorStrategy;
    }
}
