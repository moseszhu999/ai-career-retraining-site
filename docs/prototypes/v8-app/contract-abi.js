window.ProofSkillContract = {
  address: '0xProofSkillCredentialRegistryMock',
  proofStatus: {
    none: 'None',
    active: 'Active',
    revoked: 'Revoked',
    expired: 'Expired'
  },
  attestationLevel: {
    none: 'None',
    self: 'SelfAttested',
    issuer: 'IssuerAttested',
    evaluator: 'EvaluatorSigned'
  },
  functions: [
    'registerSelfAttestedProof',
    'registerIssuerAttestedProof',
    'registerEvaluatorSignedProof',
    'revokeCredential',
    'getCredentialProof',
    'verifyCredentialProof',
    'setIssuer'
  ]
};
