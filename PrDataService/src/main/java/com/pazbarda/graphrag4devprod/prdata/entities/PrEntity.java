package com.pazbarda.graphrag4devprod.prdata.entities;

import com.pazbarda.graphrag4devprod.prdata.models.PrStatus;

import java.time.LocalDateTime;

import jakarta.persistence.Entity;
import jakarta.persistence.EnumType;
import jakarta.persistence.Enumerated;
import jakarta.persistence.GeneratedValue;
import jakarta.persistence.GenerationType;
import jakarta.persistence.Id;
import jakarta.persistence.Table;

@Entity
@Table(name = "prs")
public class PrEntity {
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Integer id;
    private String repoName;
    private String prNumber;
    private LocalDateTime openedAt;
    private LocalDateTime closedAt;
    @Enumerated(EnumType.STRING)
    private PrStatus status;
    private String lastRecommendedReviewer;
    private LocalDateTime lastRecommendationAt;

    public Integer getId() {
        return id;
    }

    public void setId(Integer id) {
        this.id = id;
    }

    public String getRepoName() {
        return repoName;
    }

    public void setRepoName(String repoName) {
        this.repoName = repoName;
    }

    public String getPrNumber() {
        return prNumber;
    }

    public void setPrNumber(String prNumber) {
        this.prNumber = prNumber;
    }

    public LocalDateTime getOpenedAt() {
        return openedAt;
    }

    public void setOpenedAt(LocalDateTime openeddAt) {
        this.openedAt = openeddAt;
    }

    public LocalDateTime getClosedAt() {
        return closedAt;
    }

    public void setClosedAt(LocalDateTime closedAt) {
        this.closedAt = closedAt;
    }

    public PrStatus getStatus() {
        return status;
    }

    public void setStatus(PrStatus status) {
        this.status = status;
    }

    public String getLastRecommendedReviewer() {
        return lastRecommendedReviewer;
    }

    public void setLastRecommendedReviewer(String lastRecommendedReviewer) {
        this.lastRecommendedReviewer = lastRecommendedReviewer;
    }

    public LocalDateTime getLastRecommendationAt() {
        return lastRecommendationAt;
    }

    public void setLastRecommendationAt(LocalDateTime lastRecommendationDate) {
        this.lastRecommendationAt = lastRecommendationDate;
    }

    @Override
    public String toString() {
        return "PrEntity{" +
                "id=" + id +
                ", repoName='" + repoName + '\'' +
                ", prNumber='" + prNumber + '\'' +
                ", openeddAt=" + openedAt +
                ", closedAt=" + closedAt +
                ", status=" + status +
                ", lastRecommendedReviewer='" + lastRecommendedReviewer + '\'' +
                ", lastRecommendationDate=" + lastRecommendationAt +
                '}';
    }

    @Override
    public boolean equals(Object o) {
        if (this == o) return true;
        if (!(o instanceof PrEntity)) return false;

        PrEntity prEntity = (PrEntity) o;

        return id != null ? id.equals(prEntity.id) : prEntity.id == null;
    }

    @Override
    public int hashCode() {
        return id != null ? id.hashCode() : 0;
    }
}
