<?php

namespace App\Http\Controllers\User;

use DB;
use Auth;
use Carbon\Carbon;
use Illuminate\Http\Request;
use App\Http\Controllers\Controller;

class NotificationController extends Controller
{
    public function unread()
    {
        return response()->json(Auth::user()->unreadNotifications);
    }

    public function update(Request $request)
    {
        DB::table('notifications')
            ->where('id', $request->input('id'))
            ->update(['read_at' => Carbon::now()]);
    }

    public function all()
    {
      return response()->json([
        'unreadCount' => Auth::user()->unreadNotifications()->count(),
        'notifications' => Auth::user()->notifications
      ]);
    }

    public function markAllAsRead()
    {
      Auth::user()->unreadNotifications->markAsRead();
      return response()->json(Auth::user()->notifications);
    }
}
