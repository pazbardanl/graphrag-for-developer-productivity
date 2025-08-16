package com.pazbarda.graphrag4devprod.prdata.models;

import java.time.LocalDateTime;

public record PrDTO(
    Integer id,
    String repoName,
    String prNumber,
    LocalDateTime openedAt,
    LocalDateTime closedAt,
    PrStatus status,
    String lastRecommendedReviewer,
    LocalDateTime lastRecommendationAt
) {}
