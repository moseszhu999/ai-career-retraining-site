-- AI Agent Governance & Readiness OS v5.0.0
-- Demo tenant seed for a real Supabase environment.
-- Run after supabase/production_schema_v5.sql.

insert into clients (tenant_code, client_id, client_name, contact, service_package, contract_value, currency, status) values
('demo', 'jhc', '信华信日本业务部', '人材育成担当', 'Java新人研修 Proof Sprint', 78000, 'CNY', '进行中'),
('demo', 'bitkids', '比特顽童教育', '校区负责人', '少儿编程讲师训练包', 24000, 'CNY', '待跟进')
on conflict (tenant_code, client_id) do update set
client_name=excluded.client_name, contact=excluded.contact, service_package=excluded.service_package,
contract_value=excluded.contract_value, currency=excluded.currency, status=excluded.status, updated_at=now();

insert into cohorts (tenant_code, cohort_id, client_id, cohort_name, learner_count, start_date, end_date, trainer, status) values
('demo', 'jhc-2026-java', 'jhc', '2026 JHC Java新人训练营', 13, '2026-06-01', '2026-08-31', 'Zhu Moses', 'Week 4 进行中'),
('demo', 'bitkids-mentor-01', 'bitkids', '讲师交付能力训练 Demo', 6, '2026-07-08', '2026-07-12', 'Zhu Moses', '售前样板')
on conflict (tenant_code, cohort_id) do update set
client_id=excluded.client_id, cohort_name=excluded.cohort_name, learner_count=excluded.learner_count,
start_date=excluded.start_date, end_date=excluded.end_date, trainer=excluded.trainer, status=excluded.status, updated_at=now();

insert into learners (tenant_code, learner_id, learner_name, cohort_id, role, "group", status, progress, tasks_done, proof_files, login_alias) values
('demo', 'jhc-s01', '佐藤拓海', 'jhc-2026-java', '学员', 'A组', '进行中', 72, 3, 1, 'sato'),
('demo', 'jhc-s02', '鈴木美咲', 'jhc-2026-java', '学员', 'A组', '待Review', 81, 4, 2, 'suzuki'),
('demo', 'jhc-s03', '田中悠真', 'jhc-2026-java', '学员', 'B组', '需修改', 58, 2, 1, 'tanaka'),
('demo', 'jhc-s06', '山本結衣', 'jhc-2026-java', '学员', 'C组', '已确认', 88, 5, 3, 'yamamoto')
on conflict (tenant_code, learner_id) do update set
learner_name=excluded.learner_name, cohort_id=excluded.cohort_id, role=excluded.role, "group"=excluded."group",
status=excluded.status, progress=excluded.progress, tasks_done=excluded.tasks_done, proof_files=excluded.proof_files,
login_alias=excluded.login_alias, updated_at=now();

insert into exercises (
    tenant_code, exercise_id, module, difficulty, cohort_id, related_task, scenario, question_type,
    question, options, correct_option, explanation, required_output, hint, golden_solution, rubric,
    capability, business_process, value_chain_stage, proof_skill
) values
('demo', 'ex-login-001', '软件测试', '基础', 'jhc-2026-java', '登录功能测试用例', 'Spring Boot + Thymeleaf 登录画面测试。', '单选题',
 '下面哪一组测试用例最能补充登录功能的业务边界？',
 '["A. 只测试正确用户名、正确密码、点击登录按钮。", "B. 只测试错误密码、空用户名、空密码。", "C. 覆盖角色权限、连续失败锁定、特殊字符、超长输入、空格处理、登录后跳转。", "D. 只测试页面颜色、按钮大小、Logo 是否显示。"]'::jsonb,
 'C', '登录测试不能只覆盖正常/错误输入，还要覆盖权限、异常输入、安全边界和页面流转。', '选择最合适的测试覆盖方案；可选填写补充说明。',
 '不要只写输入正确/错误，要考虑用户角色、异常输入和登录后的页面流转。',
 '管理员登录后进入管理菜单；普通用户不能进入管理菜单；连续错误密码后锁定；异常输入不导致页面异常。',
 '选择正确80%；补充说明20%。', '测试边界识别', 'Requirement-to-Delivery Automation', 'Quality / Acceptance', '能识别登录功能测试边界'),
('demo', 'ex-order-002', '业务分析', '中级', 'jhc-2026-java', '订单状态流转拆解', '培训管理系统订单状态分析。', '单选题',
 '订单状态流转分析时，哪一个选项最完整？',
 '["A. 只需要说明未支付和已支付两个状态。", "B. 只需要说明订单金额，不需要说明课次和课耗。", "C. 需要说明创建、支付、上课扣课耗、余额变化、结课/结转，并覆盖重复支付、退费、课耗回滚、跨校区结算等异常。", "D. 只需要画一个从创建到完成的直线流程。"]'::jsonb,
 'C', '订单分析必须同时覆盖钱、课次、余额、课耗、退费、结转和跨校区结算。', '选择最合适的订单状态流转分析方案。',
 '重点看钱、课次、余额、课耗、校区结算是否一致。',
 '主流程：创建订单→支付→上课扣课耗→余额变化→结课/结转；异常：重复支付、退费、课耗回滚。',
 '选择正确75%；补充说明25%。', '订单状态分析', 'Requirement-to-Delivery Automation', 'Delivery / Execution', '能拆解订单状态和异常分支'),
('demo', 'ex-jpqa-003', '日语发表', '基础', 'jhc-2026-java', '日语Q&A发表准备', '结业发表会上遇到无法准确回答的问题。', '单选题',
 '发表会 Q&A 中，遇到自己无法准确回答的问题，最合适的日语回答是哪一个？',
 '["A. たぶん大丈夫だと思います。詳しくは分かりません。", "B. それは私の担当ではありません。", "C. 申し訳ありません。現時点では正確にお答えできないため、確認してから後ほど回答いたします。", "D. すみません、次の質問をお願いします。"]'::jsonb,
 'C', '不知道时不能乱编，应道歉、说明需要确认、承诺后续回答。', '选择最合适的日语回答。',
 '不要硬编答案。重点是诚实、确认、后续补充。',
 '申し訳ありません。現時点では正確にお答えできないため、確認してから後ほど回答いたします。',
 '选择正确80%；说明20%。', '日语风险应答', 'Training-to-Readiness Automation', 'Readiness Decision', '能在发表会中职业化回答风险问题'),
('demo', 'ex-bug-004', '错误定位', '中级', 'jhc-2026-java', 'Spring Boot错误定位报告', 'MyBatis 参数绑定失败。', '单选题',
 '面对 MyBatis 参数绑定失败，最优先排查哪一组内容？',
 '["A. 只检查页面 CSS 是否加载。", "B. 只重启服务器，看问题是否消失。", "C. 检查 Controller 参数、Service 方法、Mapper 接口 @Param、Mapper XML 中的占位符名称是否一致。", "D. 直接删除 Mapper XML 重新生成。"]'::jsonb,
 'C', 'MyBatis 参数绑定失败通常和参数名、@Param、XML 占位符、DTO 字段不一致有关。', '选择最合适的排查方向。',
 '注意 Controller 参数名、Mapper XML 参数名、DTO字段名是否一致。',
 '确认接口签名、XML、日志参数名；统一命名或补 @Param；补测试验证。',
 '选择正确75%；确认步骤和验证方法25%。', '错误定位', 'Requirement-to-Delivery Automation', 'Quality / Acceptance', '能定位 Spring/MyBatis 参数绑定问题')
on conflict (tenant_code, exercise_id) do update set
module=excluded.module, difficulty=excluded.difficulty, cohort_id=excluded.cohort_id, related_task=excluded.related_task,
scenario=excluded.scenario, question_type=excluded.question_type, question=excluded.question, options=excluded.options,
correct_option=excluded.correct_option, explanation=excluded.explanation, required_output=excluded.required_output,
hint=excluded.hint, golden_solution=excluded.golden_solution, rubric=excluded.rubric, capability=excluded.capability,
business_process=excluded.business_process, value_chain_stage=excluded.value_chain_stage, proof_skill=excluded.proof_skill, updated_at=now();

insert into assignments (tenant_code, assignment_id, exercise_id, learner_id, learner_name, cohort_id, status, assigned_at, due_date, note) values
('demo', 'asn-001', 'ex-login-001', 'jhc-s01', '佐藤拓海', 'jhc-2026-java', '已提交', '2026-06-22', '2026-06-23', '补齐登录测试边界'),
('demo', 'asn-002', 'ex-order-002', 'jhc-s02', '鈴木美咲', 'jhc-2026-java', '已提交', '2026-06-23', '2026-06-24', '订单状态流转练习'),
('demo', 'asn-003', 'ex-jpqa-003', 'jhc-s03', '田中悠真', 'jhc-2026-java', '需修改', '2026-06-24', '2026-06-25', '发表会Q&A补强'),
('demo', 'asn-004', 'ex-bug-004', 'jhc-s06', '山本結衣', 'jhc-2026-java', '已确认', '2026-06-25', '2026-06-26', '错误定位报告')
on conflict (tenant_code, assignment_id) do update set
exercise_id=excluded.exercise_id, learner_id=excluded.learner_id, learner_name=excluded.learner_name, cohort_id=excluded.cohort_id,
status=excluded.status, assigned_at=excluded.assigned_at, due_date=excluded.due_date, note=excluded.note, updated_at=now();

insert into submissions (tenant_code, submission_id, assignment_id, exercise_id, learner_id, learner_name, status, submitted_at, answer_summary, question_type, selected_option, correct_option, is_correct, auto_score, answer_note) values
('demo', 'sub-001', 'asn-001', 'ex-login-001', 'jhc-s01', '佐藤拓海', '已提交', '2026-06-23 10:20', '选择题作答：C。判定：正确；正确选项：C。', '单选题', 'C', 'C', true, 88, '补充登录测试边界。'),
('demo', 'sub-002', 'asn-002', 'ex-order-002', 'jhc-s02', '鈴木美咲', '已提交', '2026-06-24 15:40', '选择题作答：C。判定：正确；正确选项：C。', '单选题', 'C', 'C', true, 88, '订单状态覆盖较完整。'),
('demo', 'sub-003', 'asn-003', 'ex-jpqa-003', 'jhc-s03', '田中悠真', '需修改', '2026-06-25 09:15', '选择题作答：A。判定：需复习；正确选项：C。', '单选题', 'A', 'C', false, 62, '日语回答需要更礼貌和职业化。'),
('demo', 'sub-004', 'asn-004', 'ex-bug-004', 'jhc-s06', '山本結衣', '已确认', '2026-06-26 11:30', '选择题作答：C。判定：正确；正确选项：C。', '单选题', 'C', 'C', true, 88, '能识别 MyBatis 参数绑定链路。')
on conflict (tenant_code, submission_id) do update set
assignment_id=excluded.assignment_id, exercise_id=excluded.exercise_id, learner_id=excluded.learner_id, learner_name=excluded.learner_name,
status=excluded.status, submitted_at=excluded.submitted_at, answer_summary=excluded.answer_summary, question_type=excluded.question_type,
selected_option=excluded.selected_option, correct_option=excluded.correct_option, is_correct=excluded.is_correct,
auto_score=excluded.auto_score, answer_note=excluded.answer_note, updated_at=now();

insert into reviews (tenant_code, review_id, submission_id, reviewer, score, review_comment, decision, proof_ready) values
('demo', 'rev-001', 'sub-001', 'Agent', 88, '选择正确。建议补充登录后返回原访问页面的验证截图。', '待Founder确认', '候选'),
('demo', 'rev-002', 'sub-002', 'Agent', 88, '选择正确。订单状态流转和异常分支具备业务价值。', '待Founder确认', '候选'),
('demo', 'rev-003', 'sub-003', 'Agent', 62, '选择错误。遇到不知道的问题时不应含糊回答，应确认后补充。', '需复习', '否'),
('demo', 'rev-004', 'sub-004', 'Founder', 90, '证据完整，可用于客户汇报和学员发表。', '已确认', '是')
on conflict (tenant_code, review_id) do update set
submission_id=excluded.submission_id, reviewer=excluded.reviewer, score=excluded.score, review_comment=excluded.review_comment,
decision=excluded.decision, proof_ready=excluded.proof_ready, updated_at=now();

insert into proof_files (tenant_code, proof_id, learner_name, title, status, score, evidence, note) values
('demo', 'proof-001', '山本結衣', 'Spring Boot错误定位报告', '可展示', 88, '错误日志 + 修正截图 + 复盘', '适合结业发表和面试说明'),
('demo', 'proof-002', '鈴木美咲', '订单状态流转拆解', '待Review', 81, '业务流程图 + 异常分支', '等待Founder确认')
on conflict (tenant_code, proof_id) do update set
learner_name=excluded.learner_name, title=excluded.title, status=excluded.status, score=excluded.score,
evidence=excluded.evidence, note=excluded.note, updated_at=now();

insert into consult_leads (tenant_code, lead_id, client_name, package, need, status, potential_value, note) values
('demo', 'lead-001', '信华信日本业务部', '企业训练版', 'Java新人训练标准包', '已预约', 78000, '希望把3个月讲师交付沉淀成可复用训练包'),
('demo', 'lead-002', '比特顽童教育', '讲师训练版', '少儿编程讲师训练包', '新线索', 24000, '希望降低新讲师培养成本')
on conflict (tenant_code, lead_id) do update set
client_name=excluded.client_name, package=excluded.package, need=excluded.need, status=excluded.status,
potential_value=excluded.potential_value, note=excluded.note, updated_at=now();

insert into audit_logs (tenant_code, audit_id, time, actor, role, action, object_type, object_id, before_status, after_status, summary) values
('demo', 'aud-001', '2026-06-29 09:00', 'System', '系统', '初始化生产演示数据', 'System', 'demo-state', '空', '已加载', '加载 Supabase demo tenant 数据。')
on conflict (tenant_code, audit_id) do update set
time=excluded.time, actor=excluded.actor, role=excluded.role, action=excluded.action, object_type=excluded.object_type,
object_id=excluded.object_id, before_status=excluded.before_status, after_status=excluded.after_status, summary=excluded.summary;
