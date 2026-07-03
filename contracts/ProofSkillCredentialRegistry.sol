// SPDX-License-Identifier: MIT
pragma solidity ^0.8.24;

/// @title ProofSkillCredentialRegistry
/// @notice Minimal proof registry for frontend-issued, evidence-backed skill credentials.
/// @dev Stores only hashes, status, and attestation metadata. It does not store raw answers,
/// raw project files, personal data, trade documents, or AI scoring rationale.
contract ProofSkillCredentialRegistry {
    enum ProofStatus {
        None,
        Active,
        Revoked,
        Expired
    }

    enum AttestationLevel {
        None,
        SelfAttested,
        IssuerAttested,
        EvaluatorSigned
    }

    struct CredentialProof {
        bytes32 credentialId;
        bytes32 certificateHash;
        bytes32 evidenceHash;
        bytes32 scoreHash;
        bytes32 schemaHash;
        bytes32 evaluatorSetHash;
        address issuer;
        address holder;
        string credentialType;
        uint16 overallScore;
        uint64 issuedAt;
        uint64 expiresAt;
        ProofStatus status;
        AttestationLevel attestationLevel;
    }

    address public owner;

    mapping(address => bool) public authorizedIssuers;
    mapping(bytes32 => CredentialProof) private credentialProofs;

    event IssuerAuthorized(address indexed issuer, bool authorized);

    event CredentialProofRegistered(
        bytes32 indexed credentialId,
        address indexed issuer,
        address indexed holder,
        string credentialType,
        uint16 overallScore,
        bytes32 certificateHash,
        bytes32 evidenceHash,
        bytes32 scoreHash,
        bytes32 schemaHash,
        bytes32 evaluatorSetHash,
        AttestationLevel attestationLevel,
        uint64 issuedAt,
        uint64 expiresAt
    );

    event CredentialProofRevoked(
        bytes32 indexed credentialId,
        address indexed issuer,
        string reason
    );

    error NotOwner();
    error NotAuthorizedIssuer();
    error InvalidCredentialId();
    error CredentialAlreadyExists();
    error CredentialNotFound();
    error InvalidHolder();
    error InvalidExpiry();
    error InvalidEvaluatorSetHash();

    modifier onlyOwner() {
        if (msg.sender != owner) revert NotOwner();
        _;
    }

    modifier onlyAuthorizedIssuer() {
        if (!authorizedIssuers[msg.sender]) revert NotAuthorizedIssuer();
        _;
    }

    constructor() {
        owner = msg.sender;
        authorizedIssuers[msg.sender] = true;
        emit IssuerAuthorized(msg.sender, true);
    }

    function setIssuer(address issuer, bool authorized) external onlyOwner {
        authorizedIssuers[issuer] = authorized;
        emit IssuerAuthorized(issuer, authorized);
    }

    /// @notice Register a low-trust self-attested proof. Holder and issuer are both msg.sender.
    function registerSelfAttestedProof(
        bytes32 credentialId,
        string calldata credentialType,
        uint16 overallScore,
        bytes32 certificateHash,
        bytes32 evidenceHash,
        bytes32 scoreHash,
        bytes32 schemaHash,
        uint64 expiresAt
    ) external {
        _registerCredentialProof(
            credentialId,
            msg.sender,
            credentialType,
            overallScore,
            certificateHash,
            evidenceHash,
            scoreHash,
            schemaHash,
            bytes32(0),
            expiresAt,
            AttestationLevel.SelfAttested
        );
    }

    /// @notice Register an authorized issuer-attested proof.
    function registerIssuerAttestedProof(
        bytes32 credentialId,
        address holder,
        string calldata credentialType,
        uint16 overallScore,
        bytes32 certificateHash,
        bytes32 evidenceHash,
        bytes32 scoreHash,
        bytes32 schemaHash,
        uint64 expiresAt
    ) external onlyAuthorizedIssuer {
        _registerCredentialProof(
            credentialId,
            holder,
            credentialType,
            overallScore,
            certificateHash,
            evidenceHash,
            scoreHash,
            schemaHash,
            bytes32(0),
            expiresAt,
            AttestationLevel.IssuerAttested
        );
    }

    /// @notice Register the strongest proof type: authorized issuer plus evaluator signature set hash.
    function registerEvaluatorSignedProof(
        bytes32 credentialId,
        address holder,
        string calldata credentialType,
        uint16 overallScore,
        bytes32 certificateHash,
        bytes32 evidenceHash,
        bytes32 scoreHash,
        bytes32 schemaHash,
        bytes32 evaluatorSetHash,
        uint64 expiresAt
    ) external onlyAuthorizedIssuer {
        if (evaluatorSetHash == bytes32(0)) revert InvalidEvaluatorSetHash();

        _registerCredentialProof(
            credentialId,
            holder,
            credentialType,
            overallScore,
            certificateHash,
            evidenceHash,
            scoreHash,
            schemaHash,
            evaluatorSetHash,
            expiresAt,
            AttestationLevel.EvaluatorSigned
        );
    }

    /// @dev Backward-compatible alias for issuer-attested registration.
    function registerCredentialProof(
        bytes32 credentialId,
        address holder,
        string calldata credentialType,
        uint16 overallScore,
        bytes32 certificateHash,
        bytes32 evidenceHash,
        bytes32 scoreHash,
        bytes32 schemaHash,
        uint64 expiresAt
    ) external onlyAuthorizedIssuer {
        _registerCredentialProof(
            credentialId,
            holder,
            credentialType,
            overallScore,
            certificateHash,
            evidenceHash,
            scoreHash,
            schemaHash,
            bytes32(0),
            expiresAt,
            AttestationLevel.IssuerAttested
        );
    }

    function revokeCredential(bytes32 credentialId, string calldata reason) external onlyAuthorizedIssuer {
        CredentialProof storage proof = credentialProofs[credentialId];
        if (proof.status == ProofStatus.None) revert CredentialNotFound();
        if (proof.issuer != msg.sender) revert NotAuthorizedIssuer();

        proof.status = ProofStatus.Revoked;
        emit CredentialProofRevoked(credentialId, msg.sender, reason);
    }

    function getCredentialProof(bytes32 credentialId) external view returns (CredentialProof memory) {
        CredentialProof memory proof = credentialProofs[credentialId];
        if (proof.status == ProofStatus.None) revert CredentialNotFound();
        return proof;
    }

    function verifyCredentialProof(
        bytes32 credentialId,
        bytes32 certificateHash,
        bytes32 evidenceHash,
        bytes32 scoreHash,
        bytes32 schemaHash
    ) external view returns (bool valid, ProofStatus status, AttestationLevel attestationLevel) {
        CredentialProof memory proof = credentialProofs[credentialId];
        if (proof.status == ProofStatus.None) {
            return (false, ProofStatus.None, AttestationLevel.None);
        }

        ProofStatus effectiveStatus = proof.status;
        if (effectiveStatus == ProofStatus.Active && block.timestamp > proof.expiresAt) {
            effectiveStatus = ProofStatus.Expired;
        }

        bool hashMatch = proof.certificateHash == certificateHash
            && proof.evidenceHash == evidenceHash
            && proof.scoreHash == scoreHash
            && proof.schemaHash == schemaHash;

        return (hashMatch && effectiveStatus == ProofStatus.Active, effectiveStatus, proof.attestationLevel);
    }

    function _registerCredentialProof(
        bytes32 credentialId,
        address holder,
        string calldata credentialType,
        uint16 overallScore,
        bytes32 certificateHash,
        bytes32 evidenceHash,
        bytes32 scoreHash,
        bytes32 schemaHash,
        bytes32 evaluatorSetHash,
        uint64 expiresAt,
        AttestationLevel attestationLevel
    ) internal {
        if (credentialId == bytes32(0)) revert InvalidCredentialId();
        if (credentialProofs[credentialId].status != ProofStatus.None) revert CredentialAlreadyExists();
        if (holder == address(0)) revert InvalidHolder();

        uint64 issuedAt = uint64(block.timestamp);
        if (expiresAt <= issuedAt) revert InvalidExpiry();

        CredentialProof memory proof = CredentialProof({
            credentialId: credentialId,
            certificateHash: certificateHash,
            evidenceHash: evidenceHash,
            scoreHash: scoreHash,
            schemaHash: schemaHash,
            evaluatorSetHash: evaluatorSetHash,
            issuer: msg.sender,
            holder: holder,
            credentialType: credentialType,
            overallScore: overallScore,
            issuedAt: issuedAt,
            expiresAt: expiresAt,
            status: ProofStatus.Active,
            attestationLevel: attestationLevel
        });

        credentialProofs[credentialId] = proof;

        emit CredentialProofRegistered(
            credentialId,
            msg.sender,
            holder,
            credentialType,
            overallScore,
            certificateHash,
            evidenceHash,
            scoreHash,
            schemaHash,
            evaluatorSetHash,
            attestationLevel,
            issuedAt,
            expiresAt
        );
    }
}
