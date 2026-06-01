# ==============================================================================
# 1. ĐỊNH NGHĨA MỤC TIÊU CO GIÃN (SCALABLE TARGET) CHO FARGATE
# ==============================================================================
resource "aws_appautoscaling_target" "ecs_target" {
  max_capacity       = 10                                                     # Cho phép đẻ tối đa 10 container để gánh tải nặng
  min_capacity       = 2                                                      # Giữ tối thiểu 2 container lúc bình thường
  resource_id        = "service/${aws_ecs_cluster.main.name}/${aws_ecs_service.main.name}"
  scalable_dimension = "ecs:service:DesiredCount"
  service_namespace  = "ecs"
}

# ==============================================================================
# 2. CHÍNH SÁCH TỰ ĐỘNG MỞ RỘNG THEO CPU (TARGET TRACKING CPU)
# ==============================================================================
resource "aws_appautoscaling_policy" "ecs_cpu_scaling" {
  name               = "cpu-scaling"
  policy_type        = "TargetTrackingScaling"
  resource_id        = aws_appautoscaling_target.ecs_target.resource_id
  scalable_dimension = aws_appautoscaling_target.ecs_target.scalable_dimension
  service_namespace  = aws_appautoscaling_target.ecs_target.service_namespace

  target_tracking_scaling_policy_configuration {
    predefined_metric_specification {
      predefined_metric_type = "ECSServiceAverageCPUUtilization"
    }
    target_value       = 50.0  # CPU vọt qua 50% là bắt đầu kích hoạt đẻ Task

    # Cấu hình chiến lược để chạy mượt, drop độ trễ:
    scale_out_cooldown = 30    # Chỉ mất 30 giây hồi chiêu để đẻ tiếp con mới nếu vẫn quá tải
    scale_in_cooldown  = 180   # Ép giữ các con mới sống ít least 3 phút, không cho xóa vội để dẹp flapping
  }
}

# ==============================================================================
# 3. CHÍNH SÁCH TỰ ĐỘNG MỞ RỘNG THEO MEMORY (TARGET TRACKING RAM)
# ==============================================================================
resource "aws_appautoscaling_policy" "ecs_memory_scaling" {
  name               = "memory-scaling"
  policy_type        = "TargetTrackingScaling"
  resource_id        = aws_appautoscaling_target.ecs_target.resource_id
  scalable_dimension = aws_appautoscaling_target.ecs_target.scalable_dimension
  service_namespace  = aws_appautoscaling_target.ecs_target.service_namespace

  target_tracking_scaling_policy_configuration {
    predefined_metric_specification {
      predefined_metric_type = "ECSServiceAverageMemoryUtilization"
    }
    target_value       = 80.0 # RAM vọt qua 80% là đẻ thêm Task
    
    scale_out_cooldown = 30
    scale_in_cooldown  = 180
  }
}