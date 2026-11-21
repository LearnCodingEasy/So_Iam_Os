# goals security and testing

## Permission/ownership evidence

- goals/api/views/goals_views.py:L8: from rest_framework.permissions import IsAuthenticated
- goals/api/views/goals_views.py:L30: permission_classes = [IsAuthenticated]
- goals/api/views/goals_views.py:L33: def get_queryset(self):
- goals/api/views/goals_views.py:L34: queryset = (Goal.objects.filter(user=self.request.user)
- goals/api/views/goals_views.py:L60: goal = serializer.save(user=self.request.user)
- goals/api/views/goals_views.py:L67: GoalService.record(goal, self.request.user, "created", "Goal created.")
- goals/api/views/goals_views.py:L68: invalidate_dashboard(self.request.user.id)
- goals/api/views/goals_views.py:L83: GoalService.record(goal, self.request.user, "updated", "Goal details updated.")
- goals/api/views/goals_views.py:L85: GoalService.notify(self.request.user, "ØªÙ… ØªØ­Ù‚ÙŠÙ‚ Ù‡Ø¯Ù", f"Ø§ÙƒØªÙ…Ù„ Ø§Ù„Ù‡Ø¯Ù: {goal.title}", goal)
- goals/api/views/goals_views.py:L86: invalidate_dashboard(self.request.user.id)
- goals/api/views/goals_views.py:L89: GoalService.record(instance, self.request.user, "deleted", "Goal deleted.")
- goals/api/views/goals_views.py:L91: invalidate_dashboard(self.request.user.id)
- goals/api/views/goals_views.py:L95: return Response(GoalAnalyticsService.dashboard(request.user))
- goals/api/views/goals_views.py:L106: goal = GoalService.complete(self.get_object(), request.user, request.data.get("notes", ""))
- goals/api/views/goals_views.py:L109: invalidate_dashboard(request.user.id)
- goals/api/views/goals_views.py:L126: goal = GoalService.set_status(self.get_object(), new_status, request.user)
- goals/api/views/goals_views.py:L129: invalidate_dashboard(request.user.id)
- goals/api/views/goals_views.py:L137: goal = GoalService.update_progress(self.get_object(), request.data["progress_percent"], request.user)
- goals/api/views/goals_views.py:L140: invalidate_dashboard(request.user.id)
- goals/api/views/goals_views.py:L147: clone = Goal.objects.create(user=request.user, title=f"{source.title} (Copy)", description=source.description,
- goals/api/views/goals_views.py:L154: GoalService.record(clone, request.user, "duplicated", "Goal duplicated.", {"source_goal_id": source.id})
- goals/api/views/goals_views.py:L167: answer = GoalCoachService.answer(goal, request.user, message)
- goals/api/views/goals_views.py:L170: request.user.pk, goal.pk, exc.__class__.__name__)
- goals/api/views/goals_views.py:L186: request.user.pk, goal.pk)
- goals/api/views/goals_views.py:L192: GoalService.record(goal, request.user, "coach_question", "Goal Coach answered a question.", {"provider": answer.get("provider", "")})
- goals/api/views/goals_views.py:L203: goal, request.user, request.data.get("instructions", "")
- goals/api/views/goals_views.py:L207: request.user.pk, goal.pk, exc.__class__.__name__)
- goals/api/views/goals_views.py:L223: request.user.pk, goal.pk)
- goals/api/views/goals_views.py:L229: proposal = GoalPlanProposal.objects.create(goal=goal, user=request.user, payload=payload, provider=provider)
- goals/api/views/goals_views.py:L230: GoalService.record(goal, request.user, "plan_proposed", "AI generated a plan proposal. No tasks or milestones were created.", {"proposal_id": proposal.id, "provider": provider})
- goals/api/views/goals_views.py:L237: proposal = GoalPlanProposal.objects.filter(pk=proposal_id, goal=goal, user=request.user).first()
- goals/api/views/goals_views.py:L244: GoalService.record(goal, request.user, "plan_rejected", "AI plan proposal rejected.", {"proposal_id": proposal.id})
- goals/api/views/goals_views.py:L250: return Response(GoalPlanProposalSerializer(goal.plan_proposals.filter(user=request.user), many=True).data)
- goals/api/views/goals_views.py:L259: proposal = GoalPlanProposal.objects.get(pk=proposal_id, goal_id=pk, user=request.user)
- goals/api/views/goals_views.py:L260: milestones = GoalService.approve_plan(proposal, request.user)
- goals/api/views/goals_views.py:L266: invalidate_dashboard(request.user.id)
- goals/api/views/goals_views.py:L278: event = GoalService.record(goal, request.user, "note_added", note)
- goals/api/views/goals_views.py:L306: links = ProjectGoal.objects.filter(goal=goal, project__user=request.user).select_related("project")
- goals/api/views/goals_views.py:L310: project = Project.objects.filter(pk=project_id, user=request.user).first()
- goals/api/views/goals_views.py:L317: GoalService.record(goal, request.user, "project_linked", "Project linked to goal.", {"project_id": project.id})
- goals/api/views/goals_views.py:L327: permission_classes = [IsAuthenticated]
- goals/api/views/goals_views.py:L329: def get_queryset(self):
- goals/api/views/goals_views.py:L330: queryset = GoalMilestone.objects.filter(goal__user=self.request.user).select_related("goal").annotate(
- goals/api/views/goals_views.py:L340: locked_goal = Goal.objects.select_for_update().get(pk=goal.pk, user=self.request.user)
- goals/api/views/goals_views.py:L346: GoalService.record(milestone.goal, self.request.user, "milestone_created", "Milestone created.", {"milestone_id": milestone.id})
- goals/api/views/goals_views.py:L348: invalidate_dashboard(self.request.user.id)
- goals/api/views/goals_views.py:L361: GoalService.record(milestone.goal, self.request.user, "milestone_updated", "Milestone updated.", {"milestone_id": milestone.id})
- goals/api/views/goals_views.py:L363: GoalService.notify(self.request.user, "Ø§ÙƒØªÙ…Ù„Øª Ù…Ø±Ø­Ù„Ø©", f"Ø§ÙƒØªÙ…Ù„Øª Ø§Ù„Ù…Ø±Ø­Ù„Ø© {milestone.title} Ø¶Ù…Ù† Ø§Ù„Ù‡Ø¯Ù {milestone.goal.title}", milestone)
- goals/api/views/goals_views.py:L365: invalidate_dashboard(self.request.user.id)
- goals/api/views/goals_views.py:L369: GoalService.record(goal, self.request.user, "milestone_deleted", "Milestone deleted.", {"milestone_id": instance.id})
- goals/api/views/goals_views.py:L375: invalidate_dashboard(self.request.user.id)


## Tests
- goals/tests/test_goals.py
- goals/tests/__init__.py


Tests were not run. This scan is not a complete authorization/security review. Shared guidance: [authentication and permissions](../../07-authentication-and-permissions.md).
