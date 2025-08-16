package com.pazbarda.graphrag4devprod.prdata.services;

import java.time.LocalDateTime;
import java.util.List;
import java.util.stream.StreamSupport;

import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.RestController;

import com.pazbarda.graphrag4devprod.prdata.entities.PrEntity;
import com.pazbarda.graphrag4devprod.prdata.models.GetPrDataRequest;
import com.pazbarda.graphrag4devprod.prdata.models.PrDTO;
import com.pazbarda.graphrag4devprod.prdata.models.PrStatus;
import com.pazbarda.graphrag4devprod.prdata.repositories.PrRepository;
import com.pazbarda.graphrag4devprod.prdata.models.UpdatePrDataRequest;

import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PutMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestMapping;

@RestController
@RequestMapping("/prs")
public record PrController(PrRepository prRepository) {
    private static final Logger logger = LoggerFactory.getLogger(PrController.class);

    @GetMapping("/all")
    public ResponseEntity<Iterable<PrDTO>> getAllPrs() {
        Iterable<PrEntity> prEntities = prRepository.findAll();

        List<PrDTO> prDTOs = StreamSupport.stream(prEntities.spliterator(), false)
        .map(this::createPrDTOFromEntity)
        .toList();

        if (prDTOs.isEmpty()) {
            logger.info("No PRs found.");
            return ResponseEntity.noContent().build();
        }
        logger.info("Retrieved {} PRs.", prDTOs.size());
        return ResponseEntity.ok(prDTOs);
    }

    @GetMapping("/")
    public ResponseEntity<PrDTO> getPrDetails(@RequestBody GetPrDataRequest request) {
        var prEntity = prRepository.find(request.repoName(), request.prNumber());
        if (prEntity == null) {
            logger.error("PR not found for repo: {}, PR number: {}", request.repoName(), request.prNumber());
            return ResponseEntity.notFound().build();
        }
        var prDTO = createPrDTOFromEntity(prEntity);
        logger.info("Retrieved PR details for PR: {}", prDTO);
        return ResponseEntity.ok(prDTO);
    }

    @PutMapping("/")
    public ResponseEntity<Void> createNewPr(@RequestBody UpdatePrDataRequest request) {
        if (prRepository.find(request.repoName(), request.prNumber()) != null) {
            logger.error("PR already exists for repo: {}, PR number: {}", request.repoName(), request.prNumber());
            return ResponseEntity.badRequest().build();
        }
        var now = LocalDateTime.now();
        PrEntity prEntity = createPrEntityFromRequest(request, now);
        prRepository.save(prEntity);
        logger.info("Created new PR for repo: {}, PR number: {}", request.repoName(), request.prNumber());
        return ResponseEntity.ok().build();
    }

    @PutMapping("/status")
    public ResponseEntity<Void> updatePrStatus(@RequestBody UpdatePrDataRequest request) {
        var now = LocalDateTime.now();
        if (request.status() == null) {
            logger.error("PR status cannot be null for repo: {}, PR number: {}", request.repoName(), request.prNumber());
            return ResponseEntity.badRequest().build();
        }
        PrEntity prEntity = prRepository.find(request.repoName(), request.prNumber());
        if (prEntity == null) {
            logger.error("PR not found for repo: {}, PR number: {}", request.repoName(), request.prNumber());
            return ResponseEntity.notFound().build();
        }
        prEntity.setStatus(request.status());
        if (request.status() == PrStatus.OPEN) {
            prEntity.setOpenedAt(now);
        }  else if (request.status() == PrStatus.CLOSED) {
            prEntity.setClosedAt(now);
        }
        prRepository.save(prEntity);
        logger.info("Updated PR status for repo: {}, PR number: {}, status: {}", request.repoName(), request.prNumber(), request.status());
        return ResponseEntity.ok().build();
    }

    @PutMapping("/recommended-reviewer")
    public ResponseEntity<Void> updateRecommendedReviewer(@RequestBody UpdatePrDataRequest request) {
        var now = LocalDateTime.now();
        if (request.recommendedReviewer() == null || request.recommendedReviewer().isEmpty()) {
            logger.error("Recommended reviewer cannot be null or empty for repo: {}, PR number: {}", request.repoName(), request.prNumber());
            return ResponseEntity.badRequest().build();
        }
        var prEntity = prRepository.find(request.repoName(), request.prNumber());
        if (prEntity == null) {
            logger.error("PR not found for repo: {}, PR number: {}", request.repoName(), request.prNumber());
            return ResponseEntity.notFound().build();
        }
        prEntity.setLastRecommendedReviewer(request.recommendedReviewer());
        prEntity.setLastRecommendationAt(now);
        prRepository.save(prEntity);
        logger.info("Updated recommended reviewer for repo: {}, PR number: {}, recommended reviewer: {}", request.repoName(), request.prNumber(), request.recommendedReviewer());
        return ResponseEntity.ok().build();
    }

    @GetMapping("/status")
    public ResponseEntity<String> getPrStatus(@RequestBody GetPrDataRequest request) {
        var status = prRepository.getPrStatus(request.repoName(), request.prNumber());
        if (status == null) {
            logger.error("PR status not found for repo: {}, PR number: {}", request.repoName(), request.prNumber());
            return ResponseEntity.notFound().build();
        }
        logger.info("Retrieved PR status for repo {}: {}", request.repoName(), status);
        return ResponseEntity.ok(status.name());
    }

    @GetMapping("/recommended-reviewer")
    public ResponseEntity<String> getRecommendedReviewer(@RequestBody GetPrDataRequest request) {
        var reviewer = prRepository.getLastRecommendedReviewer(request.repoName(), request.prNumber());
        if (reviewer == null) {
            logger.error("Recommended reviewer not found for repo: {}, PR number: {}", request.repoName(), request.prNumber());
            return ResponseEntity.notFound().build();
        }
        logger.info("Retrieved recommended reviewer for repo {}: {}", request.repoName(), reviewer);
        return ResponseEntity.ok(reviewer);
    }

    private PrEntity createPrEntityFromRequest(UpdatePrDataRequest request, LocalDateTime now) {
        var prEntity = new PrEntity();
        var status = request.status() == null ? PrStatus.OPEN : request.status();
        prEntity.setRepoName(request.repoName());
        prEntity.setPrNumber(request.prNumber());
        prEntity.setStatus(status);
        prEntity.setOpenedAt(status == PrStatus.OPEN ? now : null);
        prEntity.setClosedAt(status == PrStatus.CLOSED ? now : null);
        prEntity.setLastRecommendedReviewer(request.recommendedReviewer());
        prEntity.setLastRecommendationAt(request.recommendedReviewer() != null ? now : null);
        return prEntity;
    }

    private PrDTO createPrDTOFromEntity(PrEntity prEntity) {
        return new PrDTO(
            prEntity.getId(),
            prEntity.getRepoName(),
            prEntity.getPrNumber(),
            prEntity.getOpenedAt(),
            prEntity.getClosedAt(),
            prEntity.getStatus(),
            prEntity.getLastRecommendedReviewer(),
            prEntity.getLastRecommendationAt()
        );
    }   
}
