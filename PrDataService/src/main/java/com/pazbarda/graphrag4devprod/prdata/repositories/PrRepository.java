package com.pazbarda.graphrag4devprod.prdata.repositories;

import org.springframework.data.jpa.repository.Query;
import org.springframework.data.repository.CrudRepository;

import com.pazbarda.graphrag4devprod.prdata.entities.PrEntity;
import com.pazbarda.graphrag4devprod.prdata.models.PrStatus;


public interface PrRepository extends CrudRepository<PrEntity, Integer> {
    @Query("SELECT p FROM PrEntity p WHERE p.repoName = :repoName AND p.prNumber = :prNumber")
    PrEntity find(String repoName, String prNumber);

    @Query("SELECT p.status FROM PrEntity p WHERE p.repoName = :repoName AND p.prNumber = :prNumber")
    PrStatus getPrStatus(String repoName, String prNumber);

    @Query("SELECT p.lastRecommendedReviewer FROM PrEntity p WHERE p.repoName = :repoName AND p.prNumber = :prNumber")
    String getLastRecommendedReviewer(String repoName, String prNumber);
}