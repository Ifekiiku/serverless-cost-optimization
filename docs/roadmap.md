# 🛣️ Roadmap – AWS Cost Optimization Advisor

This project is designed to evolve over time to cover more dimensions of AWS cost awareness and cloud hygiene. Below are planned enhancements and feature ideas.

---

## ✅ Short-Term (Planned)
- [ ] Detect unused Elastic IPs
- [ ] Add detection for stale snapshots and AMIs
- [ ] Auto-tag flagged resources with `cost-flag=true`
- [ ] Store daily findings in S3 for history and auditing

---

## 🚧 Mid-Term
- [ ] Visualize historical trends in AWS QuickSight or Athena
- [ ] Add IAM resource analyzer (unused users/roles/policies)
- [ ] Multi-region & multi-account support via AWS Organizations

---

## 🔮 Long-Term / Wishlist
- [ ] Integrate with Slack or Microsoft Teams for live cost alerts
- [ ] Add Terraform support in addition to CloudFormation
- [ ] Build UI dashboard for findings and historical costs
- [ ] Extend to GCP / Azure with provider abstraction