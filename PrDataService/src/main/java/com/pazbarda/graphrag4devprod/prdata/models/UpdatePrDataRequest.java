package com.pazbarda.graphrag4devprod.prdata.models;

public record UpdatePrDataRequest(String repoName, String prNumber, PrStatus status, String recommendedReviewer) {}
