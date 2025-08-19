package com.pazbarda.graphrag4devprod.userdata.services;

import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.RestController;

import com.pazbarda.graphrag4devprod.userdata.entities.RepoEntity;
import com.pazbarda.graphrag4devprod.userdata.models.SetRepoReviewerSelectorStrategyRequest;
import com.pazbarda.graphrag4devprod.userdata.repositories.RepoRepository;
import org.springframework.web.bind.annotation.PutMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestMapping;

@RestController
@RequestMapping("/repos")
public record RepoController(RepoRepository repoRepository) {
    private static final Logger logger = LoggerFactory.getLogger(RepoController.class);

    @GetMapping("/reviewer-selector-strategy")
    public ResponseEntity<String> getReviewerSelectorStrategy(@RequestParam String name) {
        var strategy = repoRepository.findReviewerSelectorStrategyByName(name);
        logger.debug("Retrieved reviewer selector strategy for repo {}: {}", name, strategy);
        return strategy != null 
            ? ResponseEntity.ok(strategy) 
            : ResponseEntity.notFound().build();
    }

    @PutMapping("/reviewer-selector-strategy")
    public ResponseEntity<String> setReviewerSelectorStrategy(@RequestBody SetRepoReviewerSelectorStrategyRequest request) {
        var repo = repoRepository.findByName(request.repoName());
        if (null == repo) {
            logger.info("Creating new repo with name: {}", request.repoName());
            repo = new RepoEntity();
            repo.setName(request.repoName());
        }
        repo.setReviewerSelectorStrategy(request.strategy());
        repoRepository.save(repo);
        logger.info("Set reviewer selector strategy for repo {}: {}", request.repoName(), request.strategy());
        return ResponseEntity.ok().build();   
    }
}