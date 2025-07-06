package com.pazbarda.graphrag4devprod.userdata.repositories;

import org.springframework.data.jpa.repository.Modifying;
import org.springframework.data.jpa.repository.Query;
import org.springframework.data.repository.CrudRepository;
import org.springframework.transaction.annotation.Transactional;

import com.pazbarda.graphrag4devprod.userdata.entities.Repo;

public interface RepoRepository extends CrudRepository<Repo, Integer>{

    @Query("SELECT r FROM Repo r WHERE r.name = :name")
    Repo findByName(String name);

    @Query("SELECT r.reviewerSelectorStrategy FROM Repo r WHERE r.name = :name")
    String findReviewerSelectorStrategyByName(String name);

    @Transactional
    @Modifying
    @Query("UPDATE Repo r SET r.reviewerSelectorStrategy = :strategy WHERE r.name = :repoName")
    void setReviewerSelectorStrategy(String repoName, String strategy);
}   

