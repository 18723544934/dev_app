import 'package:flutter/material.dart';
import 'package:provider/provider.dart';
import 'package:geolocator/geolocator.dart';
import 'package:flutter_animate/flutter_animate.dart';
import '../providers/category_provider.dart';
import '../services/api_service.dart';
import 'merchant_list_screen.dart';
import 'all_categories_screen.dart';

class HomeScreen extends StatefulWidget {
  const HomeScreen({super.key});

  @override
  State<HomeScreen> createState() => _HomeScreenState();
}

class _HomeScreenState extends State<HomeScreen> with TickerProviderStateMixin {
  bool _isDrawing = false;
  Map<String, dynamic>? _drawResult;
  String _location = '定位中...';

  late AnimationController _drawController;
  late Animation<double> _drawAnimation;

  @override
  void initState() {
    super.initState();
    _drawController = AnimationController(
      duration: const Duration(milliseconds: 1500),
      vsync: this,
    );
    _drawAnimation = Tween<double>(begin: 0, end: 1).animate(
      CurvedAnimation(parent: _drawController, curve: Curves.easeOut),
    );

    _loadLocation();
    context.read<CategoryProvider>().loadCategories();
  }

  @override
  void dispose() {
    _drawController.dispose();
    super.dispose();
  }

  Future<void> _loadLocation() async {
    try {
      bool serviceEnabled = await Geolocator.isLocationServiceEnabled();
      if (!serviceEnabled) {
        setState(() => _location = '定位未开启');
        return;
      }

      LocationPermission permission = await Geolocator.checkPermission();
      if (permission == LocationPermission.denied) {
        permission = await Geolocator.requestPermission();
        if (permission == LocationPermission.denied) {
          setState(() => _location = '定位权限被拒绝');
          return;
        }
      }

      Position position = await Geolocator.getCurrentPosition();
      setState(() => _location = '当前位置');
    } catch (e) {
      setState(() => _location = '定位失败');
    }
  }

  Future<void> _drawCategory() async {
    if (_isDrawing) return;

    setState(() => _isDrawing = true);
    _drawController.reset();
    _drawController.forward();

    try {
      final apiService = context.read<ApiService>();
      final result = await apiService.drawCategory(userId: 1);

      await Future.delayed(const Duration(milliseconds: 1500));

      setState(() {
        _drawResult = result;
        _isDrawing = false;
      });
    } catch (e) {
      setState(() => _isDrawing = false);
      if (mounted) {
        ScaffoldMessenger.of(context).showSnackBar(
          SnackBar(content: Text('抽取失败: $e')),
        );
      }
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      body: SafeArea(
        child: Column(
          children: [
            _buildHeader(),
            Expanded(
              child: _buildDrawArea(),
            ),
            _buildBottomNav(),
          ],
        ),
      ),
    );
  }

  Widget _buildHeader() {
    return Container(
      padding: const EdgeInsets.all(20),
      child: Row(
        children: [
          const Icon(Icons.location_on, color: Colors.orange),
          const SizedBox(width: 8),
          Text(
            _location,
            style: const TextStyle(fontSize: 16),
          ),
          const Spacer(),
          IconButton(
            icon: const Icon(Icons.history),
            onPressed: () => _showHistory(),
          ),
        ],
      ),
    );
  }

  Widget _buildDrawArea() {
    return Center(
      child: Column(
        mainAxisAlignment: MainAxisAlignment.center,
        children: [
          if (_isDrawing)
            _buildDrawingAnimation()
          else if (_drawResult != null)
            _buildResultCard()
          else
            _buildReadyCard(),
          const SizedBox(height: 40),
          _buildDrawButton(),
        ],
      ),
    );
  }

  Widget _buildDrawingAnimation() {
    return AnimatedBuilder(
      animation: _drawAnimation,
      builder: (context, child) {
        return Container(
          width: 280,
          height: 280,
          decoration: BoxDecoration(
            color: Colors.orange[50],
            borderRadius: BorderRadius.circular(20),
            border: Border.all(color: Colors.orange, width: 3),
          ),
          child: Center(
            child: Opacity(
              opacity: 1 - _drawAnimation.value,
              child: const Text(
                '抽取中...',
                style: TextStyle(fontSize: 24, color: Colors.orange),
              ),
            ),
          ),
        ).animate().scale(duration: 500.ms).then().shimmer(duration: 1000.ms);
      },
    );
  }

  Widget _buildResultCard() {
    return Container(
      width: 280,
      height: 280,
      decoration: BoxDecoration(
        color: Colors.orange[50],
        borderRadius: BorderRadius.circular(20),
        border: Border.all(color: Colors.orange, width: 3),
      ),
      child: Column(
        mainAxisAlignment: MainAxisAlignment.center,
        children: [
          Icon(Icons.restaurant, size: 80, color: Colors.orange[400]),
          const SizedBox(height: 20),
          Text(
            _drawResult!['category_name'],
            style: const TextStyle(
              fontSize: 28,
              fontWeight: FontWeight.bold,
              color: Colors.orange,
            ),
            textAlign: TextAlign.center,
          ),
          const SizedBox(height: 10),
          Text(
            '今天吃这个！',
            style: TextStyle(fontSize: 16, color: Colors.grey[600]),
          ),
        ],
      ),
    ).animate().fadeIn(duration: 500.ms).scale();
  }

  Widget _buildReadyCard() {
    return Container(
      width: 280,
      height: 280,
      decoration: BoxDecoration(
        color: Colors.grey[100],
        borderRadius: BorderRadius.circular(20),
        border: Border.all(color: Colors.grey[300]!, width: 2),
      ),
      child: Column(
        mainAxisAlignment: MainAxisAlignment.center,
        children: [
          Icon(Icons.help_outline, size: 80, color: Colors.grey[400]),
          const SizedBox(height: 20),
          Text(
            '今天吃啥？',
            style: TextStyle(
              fontSize: 28,
              fontWeight: FontWeight.bold,
              color: Colors.grey[600],
            ),
          ),
          const SizedBox(height: 10),
          Text(
            '点击下方按钮随机抽取',
            style: TextStyle(fontSize: 16, color: Colors.grey[500]),
          ),
        ],
      ),
    );
  }

  Widget _buildDrawButton() {
    if (_isDrawing) {
      return const CircularProgressIndicator(color: Colors.orange);
    }

    if (_drawResult != null) {
      return Row(
        mainAxisAlignment: MainAxisAlignment.center,
        children: [
          ElevatedButton.icon(
            onPressed: () => setState(() => _drawResult = null),
            icon: const Icon(Icons.refresh),
            label: const Text('重新抽取'),
            style: ElevatedButton.styleFrom(
              backgroundColor: Colors.grey[200],
              foregroundColor: Colors.grey[800],
              padding: const EdgeInsets.symmetric(horizontal: 24, vertical: 12),
              shape: RoundedRectangleBorder(
                borderRadius: BorderRadius.circular(30),
              ),
            ),
          ),
          const SizedBox(width: 16),
          ElevatedButton.icon(
            onPressed: _showMerchants,
            icon: const Icon(Icons.store),
            label: const Text('看看附近的店'),
            style: ElevatedButton.styleFrom(
              backgroundColor: Colors.orange,
              foregroundColor: Colors.white,
              padding: const EdgeInsets.symmetric(horizontal: 24, vertical: 12),
              shape: RoundedRectangleBorder(
                borderRadius: BorderRadius.circular(30),
              ),
            ),
          ),
        ],
      );
    }

    return ElevatedButton.icon(
      onPressed: _drawCategory,
      icon: const Icon(Icons.casino, size: 28),
      label: const Text('随机抽取', style: TextStyle(fontSize: 18)),
      style: ElevatedButton.styleFrom(
        backgroundColor: Colors.orange,
        foregroundColor: Colors.white,
        padding: const EdgeInsets.symmetric(horizontal: 40, vertical: 16),
        shape: RoundedRectangleBorder(
          borderRadius: BorderRadius.circular(30),
        ),
      ),
    ).animate().fadeIn().scale();
  }

  Widget _buildBottomNav() {
    return Container(
      padding: const EdgeInsets.all(20),
      child: Row(
        mainAxisAlignment: MainAxisAlignment.spaceEvenly,
        children: [
          _buildNavItem(
            icon: Icons.grid_view,
            label: '全部菜系',
            onTap: () => Navigator.push(
              context,
              MaterialPageRoute(builder: (_) => const AllCategoriesScreen()),
            ),
          ),
          _buildNavItem(
            icon: Icons.settings,
            label: '设置',
            onTap: () {},
          ),
        ],
      ),
    );
  }

  Widget _buildNavItem({
    required IconData icon,
    required String label,
    required VoidCallback onTap,
  }) {
    return InkWell(
      onTap: onTap,
      borderRadius: BorderRadius.circular(12),
      child: Container(
        padding: const EdgeInsets.symmetric(horizontal: 20, vertical: 12),
        child: Column(
          mainAxisSize: MainAxisSize.min,
          children: [
            Icon(icon, color: Colors.grey[700]),
            const SizedBox(height: 4),
            Text(
              label,
              style: TextStyle(color: Colors.grey[700], fontSize: 12),
            ),
          ],
        ),
      ),
    );
  }

  void _showMerchants() async {
    if (_drawResult == null) return;

    try {
      Position position = await Geolocator.getCurrentPosition();
      if (mounted) {
        Navigator.push(
          context,
          MaterialPageRoute(
            builder: (_) => MerchantListScreen(
              categoryId: _drawResult!['category_id'],
              categoryName: _drawResult!['category_name'],
              longitude: position.longitude,
              latitude: position.latitude,
            ),
          ),
        );
      }
    } catch (e) {
      if (mounted) {
        ScaffoldMessenger.of(context).showSnackBar(
          SnackBar(content: Text('获取位置失败: $e')),
        );
      }
    }
  }

  void _showHistory() async {
    try {
      final apiService = context.read<ApiService>();
      final history = await apiService.getDrawHistory(1);

      if (mounted) {
        showModalBottomSheet(
          context: context,
          builder: (context) => Container(
            padding: const EdgeInsets.all(20),
            child: Column(
              mainAxisSize: MainAxisSize.min,
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                const Text(
                  '抽取历史',
                  style: TextStyle(fontSize: 20, fontWeight: FontWeight.bold),
                ),
                const SizedBox(height: 20),
                if (history.isEmpty)
                  const Text('暂无历史记录')
                else
                  ...history.map((item) => ListTile(
                        leading: const Icon(Icons.history),
                        title: Text(item['category_name']),
                        subtitle: Text(item['draw_time']),
                      )),
              ],
            ),
          ),
        );
      }
    } catch (e) {
      if (mounted) {
        ScaffoldMessenger.of(context).showSnackBar(
          SnackBar(content: Text('获取历史失败: $e')),
        );
      }
    }
  }
}
